#!/bin/bash

# Author: Kiyoon Kim (yoonkr33@gmail.com)
# Date: 20161228
# Using downsample_img.py, downsample multiple images in a directory.

if [ $# -lt 1 ]
then
	echo "Usage: bash $0 [dir]"
	echo "Make sure you backup the directory!"
	echo
	echo "makes LR images"
	echo "Author: Kiyoon Kim (yoonkr33@gmail.com)"
	exit 1
fi

PARALLEL=10

if [ -f "$1/.things_to_downsample.log" ]
then
	files=$(diff "$1/.downsample_completed.log" "$1/.things_to_downsample.log" | grep ">" | sed -e 's/> //')
else
	files=$(find "$1" -type f -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.bmp" -o -iname "*.gif")
fi

total=$(echo "$files" | wc -l)
i=0
parallel=0

\rm "$1/.downsampling.log"
\mv "$1/.downsample_completed.log" "$1/.downsample_completed.log.old"
\mv "$1/.things_to_downsample.log" "$1/.things_to_downsample.log.old"
echo "$files" > "$1/.things_to_downsample.log"
echo "$files" | while read -r line
do
	col=$(tput cols)
	(( i++ ))
	(( parallel++ ))
	printf '%*s' $col "($i/$total)" 
	echo -ne "\rProcessing $line..\r"
	python2 downsample_img.py "$line" &
	echo "$line" >> "$1/.downsampling.log"

	if [ $parallel -ge $PARALLEL ] || [ $i -ge $total ]
	then
		parallel=0
		wait
		cat "$1/.downsampling.log" >> "$1/.downsample_completed.log"
		\rm "$1/.downsampling.log"
	fi
done

echo
echo "Processing done!"
