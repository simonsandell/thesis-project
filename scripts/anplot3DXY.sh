#!/bin/bash
# loop over raw data files, do data analysis on them by calling analyzeData.py 
for filename in ./output/3DXY/*; do
	echo "analyzing $filename"
	python3 ../scripts/analyze3DXY.py $(basename $filename)
	python3 ../scripts/L_analyze3DXY.py $(basename $filename)
done
