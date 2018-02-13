#!/bin/bash

for filename in ./teqoutput/*; do
	python3 ../scripts/teqanalyze.py $(basename $filename)
done
../scripts/tplots.sh
