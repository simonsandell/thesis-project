#!/bin/bash
# loop over raw data files, do data analysis on them by calling analyzeData.py 
for filename in ./output/*; do
	python3 analyzeData.py $(basename $filename)
done

#Display a selection of plots from the output of analyzeData.py using xmgrace

enstring=""
for filename in ./foutput/en/*; do
	enstring="$enstring -settype xydy $filename"
done
xmgrace $enstring -nosafe -noask -pexec 'xaxis label "Temp"' -pexec 'yaxis label "Energy"' &

magstring=""
for filename in ./foutput/mag/*; do
	magstring="$magstring -settype xydy $filename"
done
xmgrace $magstring -nosafe -noask -pexec 'xaxis label "Temp"' -pexec 'yaxis label "Magnetization"' &

teqstring=""
for filename in ./foutput/teq/*; do
	teqstring="$teqstring -settype xydy $filename"
done
xmgrace $teqstring -log x -pexec 'xaxis label "N_equil"' -pexec 'yaxis label "Magnetization"' -nosafe -noask &

binstring=""
for filename in ./foutput/bin/*; do
	binstring="$binstring -settype xydy $filename"
done
xmgrace $binstring -nosafe -noask -pexec 'xaxis label "Temp"' -pexec 'yaxis label "Binder Cumulant"' &

dbdtstring=""
for filename in ./foutput/dbdt/*; do
	dbdtstring="$dbdtstring -settype xydy $filename"
done
xmgrace $dbdtstring -nosafe -noask -pexec 'xaxis label "Temp"' -pexec 'yaxis label "dB/dT"' &

xistring=""
for filename in ./foutput/xi/*; do
	xistring="$xistring -settype xydy $filename"
done
xmgrace $xistring -nosafe -noask -pexec 'xaxis label "Temp"' -pexec 'yaxis label "Susceptibility"' &

rsstring=""
for filename in ./foutput/rs/*; do
	rsstring="$rsstring -settype xydy $filename"
done
xmgrace $rsstring -nosafe -noask -pexec 'xaxis label "Temp"' -pexec 'yaxis label "Superfluid density"' &

