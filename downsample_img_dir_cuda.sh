#!/bin/bash

# Author: Kiyoon Kim (yoonkr33@gmail.com)
# Date: 20161228
# Using downsample_img.py, downsample multiple images in a directory.

if [ $# -lt 2 ]
then
	echo "Usage: bash $0 [dir] [mode=crop or squeeze]"
	echo "Make sure you backup the directory!"
	echo
	echo "makes LR images"
	echo "Author: Kiyoon Kim (yoonkr33@gmail.com)"
	exit 1
fi


if [ -f "$1/.things_to_downsample.log" ]
then
	files=$(diff "$1/.downsample_completed.log" "$1/.things_to_downsample.log" | grep ">" | sed -e 's/> //')
else
	files=$(find "$1" -type f -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.bmp" -o -iname "*.gif")
fi

\rm "$1/.downsampling.log"
\mv "$1/.downsample_completed.log" "$1/.downsample_completed.log.old"
\mv "$1/.things_to_downsample.log" "$1/.things_to_downsample.log.old"
echo "$files" > "$1/.things_to_downsample.log"
python2 downsample_img_cuda.py "$1/.things_to_downsample.log" "$1/.downsample_completed.log" $2
echo
echo "Processing done!"
