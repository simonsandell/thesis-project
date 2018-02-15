#!/bin/bash
# loop over raw data files, do data analysis on them by calling analyzeData.py 
for filename in ./output/*; do
	echo "analyzing $filename"
	python3 ../scripts/analyzeData.py $(basename $filename)
done
../scripts/rplots.sh
