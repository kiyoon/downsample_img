#!/usr/bin/env python

# Author: Kiyoon Kim (yoonkr33@gmail.com)
# Date: 20161228
# Make an image cropped, and downsampled as 16x12.
# BE SURE TO BACKUP THE ORIGINAL IMAGE!!

import sys
import os

if len(sys.argv) < 2:
    print("Usage: python2 %s [text file of image_file_list] [path_to_log_output] [mode (either crop or squeeze)]" % sys.argv[0]) 
    sys.exit()

# definitions
OUTPUT_WIDTH = 16
OUTPUT_HEIGHT = 12


import numpy as np
import cv2
from operator import add

import pycuda.driver as drv
import pycuda.autoinit
from pycuda.compiler import SourceModule

if sys.argv[3] not in ('crop', 'squeeze'):
    raise ValueError("mode should be crop or squeeze. got " + sys.argv[3])

mod = SourceModule("""
#define IDX_OUT(xx,yy,zz) ((zz) + blockDim.z * (yy) + blockDim.z*blockDim.y*(xx))
#define IDX_IN(xx,yy,zz) ((zz) + blockDim.z * (yy) + blockDim.z*blockDim.y*nRegionW*(xx))
__global__ void average_block(unsigned char* inp, unsigned char* out, int nRegionW, int nRegionH)
{
    const int x = threadIdx.x;
    const int y = threadIdx.y;
    const int z = threadIdx.z;
    int val = 0;
    for(int i = x*nRegionH; i < (x+1)*nRegionH; i++)
        for(int j = y*nRegionW; j < (y+1)*nRegionW; j++)
            val += inp[IDX_IN(i,j,z)];
    val /= nRegionW * nRegionH;
    out[IDX_OUT(x,y,z)] = (char)val;
}
""")        

average_block = mod.get_function("average_block")



num_files = sum(1 for line in open(sys.argv[1], 'r'))
idx_files = 0

log = open(sys.argv[2], 'a')
with open(sys.argv[1], 'r') as f:
    for imgfile in f:
        imgfile = imgfile.strip()
        idx_files += 1
        print("Processing %s..\t(%d/%d)" % (imgfile, idx_files, num_files))

        img = cv2.imread(imgfile)
        height, width, channels = img.shape
        
        if height == OUTPUT_HEIGHT and width == OUTPUT_WIDTH:
            # already low resolution
            log.write(imgfile)
            log.write('\n')
            continue

        # if the image is smaller than output, enhance
        if width < OUTPUT_WIDTH:
            scale = OUTPUT_WIDTH / width
            height = int(height * scale)
            img = cv2.resize(img, (OUTPUT_WIDTH, height))
            width = OUTPUT_WIDTH
        elif height < OUTPUT_HEIGHT:
            scale = OUTPUT_HEIGHT/ height
            width = int(width * scale)
            img = cv2.resize(img, (width, OUTPUT_HEIGHT))
            height = OUTPUT_HEIGHT
           
        ## First crop. Make width and height proportional to 16 and 12
        ##
        first_crop_width = width % OUTPUT_WIDTH   # number of pixels to drop, to make it proportional to 16
        first_crop_height = height % OUTPUT_HEIGHT   # number of pixels to drop, to make it proportional to 12
        #print height, width, channels
        #print first_crop_width
        #print first_crop_height
        
        if first_crop_width != 0:
            img = img[:, first_crop_width // 2 : -(first_crop_width // 2 + first_crop_width % 2)]
        if first_crop_height != 0:
            img = img[first_crop_height // 2 : -(first_crop_height // 2 + first_crop_height % 2), :]
        
        height, width, channels = img.shape
        #print height, width, channels
        
        ## Second crop. Make the ratio same as OUTPUT_WIDTH and OUTPUT_HEIGHT ratio (4:3 here)
        ##
        region_height = height // OUTPUT_HEIGHT
        region_width = width // OUTPUT_WIDTH

        if sys.argv[3] == 'crop':
            if region_height > region_width:
                # crop height
                n_crop_region = region_height - region_width    # number of regions to be cropped
                n_crop_pixel = n_crop_region * OUTPUT_HEIGHT    # number of pixels to be cropped
                img = img[n_crop_pixel // 2 : -(n_crop_pixel // 2 + n_crop_pixel % 2), :]
                region_height = region_width
            
            elif region_height < region_width:
                # crop width
                n_crop_region = region_width - region_height    # number of regions to be cropped
                n_crop_pixel = n_crop_region * OUTPUT_WIDTH     # number of pixels to be cropped
                img = img[:, n_crop_pixel // 2 : -(n_crop_pixel // 2 + n_crop_pixel % 2)]
                region_width = region_height
        
        # now, region is square.


        # if region is unity, already changed to LR
        if region_width == 1 and region_height == 1:
            os.unlink(imgfile)
            cv2.imwrite(imgfile, img)
            log.write(imgfile)
            log.write('\n')
            continue
        
        height, width, channels = img.shape
        #print height, width, channels
        
        LR_img = np.zeros((OUTPUT_HEIGHT, OUTPUT_WIDTH, 3), np.uint8)   # Initialized to black image. Add color later
        img = np.ascontiguousarray(img,dtype=np.uint8)
        
        average_block(drv.In(img), drv.Out(LR_img), np.int32(region_width), np.int32(region_height), grid=(1,1), block=(OUTPUT_HEIGHT,OUTPUT_WIDTH,3))
        
        os.unlink(imgfile)
        cv2.imwrite(imgfile, LR_img)
        log.write(imgfile)
        log.write('\n')
            
            
        
        
        #cv2.imshow("second crop",img)
        #cv2.waitKey(0)
        #cv2.imshow("final LR image", LR_img)
        #cv2.waitKey(0)
