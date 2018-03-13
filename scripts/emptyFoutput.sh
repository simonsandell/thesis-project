#!/bin/bash
echo "Delete files matching *$1*  in ./foutput/*/?"
read answer
if [ $answer != "Y" ]; then
	echo "answer 'Y' if you want to delete"
	exit 1;
fi
for dir in ./foutput/*/; do
	for subdir in $dir/*/; do
		for file in $subdir/*$1*; do
			rm $file
		done
	done
done
