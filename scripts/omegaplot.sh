#!/bin/bash

teqstring="-param ../scripts/default.par"
for filename in ./foutput/3DXY/omega/*; do
	teqstring="$teqstring -settype xydy $filename"
done
xmgrace $teqstring -pexec 'xaxis label "Temperature"' -pexec 'yaxis label "scaling correction omega"' -nosafe -noask -legend load &
