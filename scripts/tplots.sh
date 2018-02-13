#!/bin/bash

teqstring="-param ../scripts/default.par"
for filename in ./foutput/teq/*; do
	teqstring="$teqstring -settype xydy $filename"
done
xmgrace $teqstring -log x -pexec 'xaxis label "N_equil_sweeps"' -pexec 'yaxis label "Magnetization"' -nosafe -noask -legend load &
