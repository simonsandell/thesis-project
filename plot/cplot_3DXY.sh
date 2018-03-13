#!/bin/bash

omegastring="-param ../scripts/default.par"
for filename in ./foutput/3DXY/omega/*; do
	omegastring="$omegastring -settype xydy $filename"
done
xmgrace $omegastring -pexec 'xaxis label "Temperature"' -pexec 'yaxis label "omega"' -nosafe -noask -free -legend load &

rsstring="-param ../scripts/default.par"
for filename in ./foutput/3DXY/rs_corr/*; do
	rsstring="$rsstring -settype xydy $filename"
done
xmgrace $rsstring -pexec 'xaxis label "Temperature"' -pexec 'yaxis label "rho_s corr"' -nosafe -noask -free -legend load &
