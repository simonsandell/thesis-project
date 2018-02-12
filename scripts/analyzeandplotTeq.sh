#!/bin/bash

for filename in ./teqoutput/*; do
	python3 ../scripts/teqanalyze.py $(basename $filename)
done

teqstring="-param ../scripts/default.par"
for filename in ./foutput/teq/*; do
	teqstring="$teqstring -settype xydy $filename"
done
xmgrace $teqstring -log x -pexec 'xaxis label "N_equil_sweeps"' -pexec 'yaxis label "Magnetization"' -nosafe -noask -legend load &
