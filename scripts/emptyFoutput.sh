#!/bin/bash
echo "Delete all files in ./foutput/?"
read answer
if [ $answer != "Y" ]; then
	echo "answer 'Y' if you want to delete"
	exit 1;
fi
for dir in ./foutput/*/; do
	for file in $dir/*; do
		rm $file
	done
done
