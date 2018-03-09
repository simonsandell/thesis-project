#!/bin/bash
# loop over raw data files, do data analysis on them by calling analyzeData.py 
for filename in ./output/Ising3D/*; do
	echo "analyzing $filename"
	python3 ../scripts/analyzeIsing3D.py $(basename $filename)
	python3 ../scripts/L_analyzeIsing3D.py $(basename $filename)
done
