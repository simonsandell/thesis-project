#!/bin/bash

for filename in ./teqoutput/*; do
	python3 ../scripts/newteqana.py $(basename $filename)
done
../scripts/ntplots.sh
