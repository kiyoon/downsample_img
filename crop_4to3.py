#!/usr/bin/env python

# Author: Kiyoon Kim (yoonkr33@gmail.com)
# Date: 20161228
# Make an image cropped to fit 4:3 ratio
# BE SURE TO BACKUP THE ORIGINAL IMAGE!!

import sys
import os

if len(sys.argv) < 3:
    print("Usage: python2 %s [text file of image_file_list] [path_to_log_output]" % sys.argv[0]) 
    sys.exit()

# definitions
RATIO_WIDTH = 4
RATIO_HEIGHT = 3


import numpy as np
import cv2
from operator import add

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
        
        if height == RATIO_HEIGHT and width == RATIO_WIDTH:
            # already low resolution
            log.write(imgfile)
            log.write('\n')
            continue

        # if the image is smaller than output, enhance
        if width < RATIO_WIDTH:
            scale = RATIO_WIDTH / width
            height = int(height * scale)
            img = cv2.resize(img, (RATIO_WIDTH, height))
            width = RATIO_WIDTH
        elif height < RATIO_HEIGHT:
            scale = RATIO_HEIGHT/ height
            width = int(width * scale)
            img = cv2.resize(img, (width, RATIO_HEIGHT))
            height = RATIO_HEIGHT
           
        ## First crop. Make width and height proportional to 16 and 12
        ##
        first_crop_width = width % RATIO_WIDTH   # number of pixels to drop, to make it proportional to 16
        first_crop_height = height % RATIO_HEIGHT   # number of pixels to drop, to make it proportional to 12
        #print height, width, channels
        #print first_crop_width
        #print first_crop_height
        
        if first_crop_width != 0:
            img = img[:, first_crop_width // 2 : -(first_crop_width // 2 + first_crop_width % 2)]
        if first_crop_height != 0:
            img = img[first_crop_height // 2 : -(first_crop_height // 2 + first_crop_height % 2), :]
        
        height, width, channels = img.shape
        #print height, width, channels
        
        ## Second crop. Make the ratio same as RATIO_WIDTH and RATIO_HEIGHT ratio (4:3 here)
        ##
        region_height = height // RATIO_HEIGHT
        region_width = width // RATIO_WIDTH

        if region_height > region_width:
            # crop height
            n_crop_region = region_height - region_width    # number of regions to be cropped
            n_crop_pixel = n_crop_region * RATIO_HEIGHT    # number of pixels to be cropped
            img = img[n_crop_pixel // 2 : -(n_crop_pixel // 2 + n_crop_pixel % 2), :]
            region_height = region_width
        
        elif region_height < region_width:
            # crop width
            n_crop_region = region_width - region_height    # number of regions to be cropped
            n_crop_pixel = n_crop_region * RATIO_WIDTH     # number of pixels to be cropped
            img = img[:, n_crop_pixel // 2 : -(n_crop_pixel // 2 + n_crop_pixel % 2)]
            region_width = region_height
    
        # now, region is square.
        
        os.unlink(imgfile)
        cv2.imwrite(imgfile, img)
        log.write(imgfile)
        log.write('\n')
            
