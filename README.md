# Downsample_img

## Author
Kiyoon Kim  
http://kiyoon.kim  
http://sparkware.co.kr  
im@kiyoon.kim

## Description

Image downsampler written in Python2. Tested on Ubuntu 16.04 LTS. Supports CPU and GPU parallelization. Downsample based on averaging pixels, and crops if ratio doesn't fit. CUDA supports mode 'squeeze' to squeeze if the radio doesn't fit.

Make sure you copy the original data and run it, otherwise you'll lose your data. Hardlinks will be unlinked, so you can just do

```cp -al original_HR new_LR```
and run with "new_LR"


## Running the code

### Single image

Simply run the code in bash:  
```bash
./downsample_img.py [img_path]
```
Will NOT back up the original image, so it's your job to do so.

### Multiple images

- Without parallelization  

Put every images in a single directory and run  
```bash
./downsample_img_dir.sh [dir_path]
```
- To enable CPU parallelization (faster), run  
```bash
./downsample_img_dir_parallel.sh [dir_path]
```
Default number of processes is set to 10.  

- To enable GPU CUDA parallelization (fastest), run  

```bash
./downsample_img_dir_cuda.sh [dir_path] [mode (crop or squeeze)]
```
