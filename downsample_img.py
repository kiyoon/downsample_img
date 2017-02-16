#!/usr/bin/env python

# Author: Kiyoon Kim (yoonkr33@gmail.com)
# Date: 20161228
# Make an image cropped, and downsampled as 16x12.
# BE SURE TO BACKUP THE ORIGINAL IMAGE!!

import sys

if len(sys.argv) < 2:
    print("Usage: python2 %s [image_file]" % sys.argv[0]) 
    sys.exit()

# definitions
OUTPUT_WIDTH = 16
OUTPUT_HEIGHT = 12


import numpy as np
import cv2
from operator import add

img = cv2.imread(sys.argv[1])
height, width, channels = img.shape

if height == OUTPUT_HEIGHT and width == OUTPUT_WIDTH:
    # already low resolution
    sys.exit()

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
region_wh = region_width    # width and height will eventually be same, so it is the value of final region size (width and rectangle)

if region_height > region_width:
    # crop height
    n_crop_region = region_height - region_width    # number of regions to be cropped
    n_crop_pixel = n_crop_region * OUTPUT_HEIGHT    # number of pixels to be cropped
    img = img[n_crop_pixel // 2 : -(n_crop_pixel // 2 + n_crop_pixel % 2), :]

elif region_height < region_width:
    # crop width
    n_crop_region = region_width - region_height    # number of regions to be cropped
    n_crop_pixel = n_crop_region * OUTPUT_WIDTH     # number of pixels to be cropped
    img = img[:, n_crop_pixel // 2 : -(n_crop_pixel // 2 + n_crop_pixel % 2)]
    region_wh = region_height

# now, region is square.

# if region is unity, already changed to LR
if region_wh == 1:
    os.unlink(sys.argv[1])
    cv2.imwrite(sys.argv[1], img)
    sys.exit()

height, width, channels = img.shape
#print height, width, channels

LR_img = np.zeros((OUTPUT_HEIGHT, OUTPUT_WIDTH, 3), np.uint32)   # Initialized to black image. Add color later
for i in range(OUTPUT_HEIGHT):
    for j in range(OUTPUT_WIDTH):
        img_region = img[i*region_wh:(i+1)*region_wh, j*region_wh:(j+1)*region_wh]
        for tmp in img_region:
            for BGR in tmp:
                LR_img[i,j,0] += BGR[0]
                LR_img[i,j,1] += BGR[1]
                LR_img[i,j,2] += BGR[2]
                #LR_img[i,j] = map(add, LR_img[i,j], BGR)
        LR_img[i,j] /= pow(region_wh,2)
        #height, width, channels = img_region.shape
        #print height, width, channels
        #print LR_img[i,j]

LR_img = LR_img.astype(np.uint8)
os.unlink(sys.argv[1])
cv2.imwrite(sys.argv[1], LR_img)

#cv2.imshow("second crop",img)
#cv2.waitKey(0)
#cv2.imshow("final LR image", LR_img)
#cv2.waitKey(0)
