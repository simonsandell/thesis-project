#!/bin/bash
for file in ./splitted/*; do
	echo "sorting $file"
	sort $file -o $file
done
