#!/bin/bash

# Author: Kiyoon Kim (yoonkr33@gmail.com)
# Date: 20161228
# Using crop_4to3.py, crop images to fit 4:3 ratio

if [ $# -lt 1 ]
then
	echo "Usage: bash $0 [dir]"
	echo "Make sure you backup the directory!"
	echo
	echo "makes images cropped to fit 4:3 ratio"
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
python2 crop_4to3.py "$1/.things_to_downsample.log" "$1/.downsample_completed.log"
echo
echo "Processing done!"
