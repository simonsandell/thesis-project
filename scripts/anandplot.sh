#!/bin/bash
# format data from output
for filename in ./output/*; do
	python3 analyzeData.py $(basename $filename)
done

#display plots

enstring=""
for filename in ./foutput/en/*; do
	enstring="$enstring -settype xydy $filename"
done
xmgrace $enstring -nosafe -pexec 'xaxis label "Temp"' -pexec 'yaxis label "Energy"' &

magstring=""
for filename in ./foutput/mag/*; do
	magstring="$magstring -settype xydy $filename"
done
xmgrace $magstring -nosafe -pexec 'xaxis label "Temp"' -pexec 'yaxis label "Magnetization"' &

teqstring=""
for filename in ./foutput/teq/*; do
	teqstring="$teqstring -settype xydy $filename"
done
xmgrace $teqstring -log x -pexec 'xaxis label "N_equil"' -pexec 'yaxis label "Magnetization"' -nosafe -noask &

binstring=""
for filename in ./foutput/bin/*; do
	binstring="$binstring -settype xydy $filename"
done
xmgrace $binstring -nosafe -pexec 'xaxis label "Temp"' -pexec 'yaxis label "Binder Cumulant"' &

dbdtstring=""
for filename in ./foutput/dbdt/*; do
	dbdtstring="$dbdtstring -settype xydy $filename"
done
xmgrace $dbdtstring -nosafe -pexec 'xaxis label "Temp"' -pexec 'yaxis label "dB/dT"' &

xistring=""
for filename in ./foutput/xi/*; do
	xistring="$xistring -settype xydy $filename"
done
xmgrace $xistring -nosafe -pexec 'xaxis label "Temp"' -pexec 'yaxis label "Susceptibility"' &

