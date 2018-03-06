#!/bin/bash
for filename in ./foutput/L_bin/*; do
	python3 ../scripts/calcomega.py $filename
done
../scripts/omegaplot.sh
