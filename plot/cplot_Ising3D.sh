#!/bin/bash

omegastring="-param ../scripts/default.par"
for filename in ./foutput/Ising3D/omega/*; do
	omegastring="$omegastring -settype xydy $filename"
done
xmgrace $omegastring -pexec 'xaxis label "Temperature"' -pexec 'yaxis label "omega"' -nosafe -noask -free -legend load &

