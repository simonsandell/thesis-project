#!/bin/bash
#Display a selection of plots from the output of analyzeData.py using xmgrace

enstring="-param ../scripts/default.par"
for filename in ./foutput/en/*; do
	enstring="$enstring -settype xydy $filename"
done
xmgrace $enstring -nosafe -noask -legend load -pexec 'xaxis label "Temp"' -pexec 'yaxis label "Energy"' &

magstring="-param ../scripts/default.par"
for filename in ./foutput/mag/*; do
	magstring="$magstring -settype xydy $filename"
done
xmgrace $magstring -nosafe -noask -legend load -pexec 'xaxis label "Temp"' -pexec 'yaxis label "Magnetization"' &


binstring="-param ../scripts/default.par"
for filename in ./foutput/bin/*; do
	binstring="$binstring -settype xydy $filename"
done
xmgrace $binstring -nosafe -noask -legend load -pexec 'xaxis label "Temp"' -pexec 'yaxis label "Binder Cumulant"' &

dbdtstring="-param ../scripts/default.par"
for filename in ./foutput/dbdt/*; do
	dbdtstring="$dbdtstring -settype xydy $filename"
done
xmgrace $dbdtstring -nosafe -noask -legend load -pexec 'xaxis label "Temp"' -pexec 'yaxis label "dB/dT"' &

xistring="-param ../scripts/default.par"
for filename in ./foutput/xi/*; do
	xistring="$xistring -settype xydy $filename"
done
xmgrace $xistring -nosafe -noask -legend load -pexec 'xaxis label "Temp"' -pexec 'yaxis label "Susceptibility"' &

rsstring="-param ../scripts/default.par"
for filename in ./foutput/rs/*; do
	rsstring="$rsstring -settype xydy $filename"
done
xmgrace $rsstring -nosafe -noask -legend load -pexec 'xaxis label "Temp"' -pexec 'yaxis label "Superfluid density"' &


