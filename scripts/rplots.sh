#!/bin/bash
#Display a selection of plots from the output of analyzeData.py using xmgrace

#Binder paramter
binstring="-param ../scripts/default.par"
for filename in ./foutput/bin/*; do
	binstring="$binstring -settype xydy $filename"
done
xmgrace $binstring -nosafe -noask -legend load -pexec 'xaxis label "Temp"' -pexec 'yaxis label "Binder Cumulant"' &

#Superfluid density
rsstring="-param ../scripts/default.par"
for filename in ./foutput/rs/*; do
	rsstring="$rsstring -settype xydy $filename"
done
xmgrace $rsstring -nosafe -noask -legend load -pexec 'xaxis label "Temp"' -pexec 'yaxis label "Superfluid density"' &

#Only plot rest if requested
if [ ! $# -eq 0 ]
then
	#Energy per spin
	enstring="-param ../scripts/default.par"
	for filename in ./foutput/en/*$1*; do
		enstring="$enstring -settype xydy $filename"
	done
	xmgrace $enstring -nosafe -noask -legend load -pexec 'xaxis label "Temp"' -pexec 'yaxis label "Energy"' &

	#Magnetization per spin
	magstring="-param ../scripts/default.par"
	for filename in ./foutput/mag/*$1*; do
		magstring="$magstring -settype xydy $filename"
	done
	xmgrace $magstring -nosafe -noask -legend load -pexec 'xaxis label "Temp"' -pexec 'yaxis label "Magnetization"' &


	#dB/dT
	dbdtstring="-param ../scripts/default.par"
	for filename in ./foutput/dbdt/*$1*; do
		dbdtstring="$dbdtstring -settype xydy $filename"
	done
	xmgrace $dbdtstring -nosafe -noask -legend load -pexec 'xaxis label "Temp"' -pexec 'yaxis label "dB/dT"' &
	#Susceptibility
	xistring="-param ../scripts/default.par"
	for filename in ./foutput/xi/*$1*; do
		xistring="$xistring -settype xydy $filename"
	done
	xmgrace $xistring -nosafe -noask -legend load -pexec 'xaxis label "Temp"' -pexec 'yaxis label "Susceptibility"' &
fi

