#!/bin/bash
#Display a selection of plots from the output of analyzeData.py using xmgrace

#Only plot rest if requested
if [ ! $# -eq 0 ]
then
	#Binder paramter
	binstring="-param ../scripts/default.par"
	for filename in ./foutput/bin/*$1*; do
		binstring="$binstring -settype xydy $filename"
	done
	xmgrace $binstring -nosafe -noask -legend load -pexec 'xaxis label "Temp"' -pexec 'yaxis label "Binder Cumulant"' &
	
	#heatcap
	rsstring="-param ../scripts/default.par"
	for filename in ./foutput/c/*$1*; do
		rsstring="$rsstring -settype xydy $filename"
	done
	xmgrace $rsstring -nosafe -noask -legend load -pexec 'xaxis label "Temp"' -pexec 'yaxis label "Heat capacity"' &
	
	#Energy per spin
	enstring="-param ../scripts/default.par"
	for filename in ./foutput/en/*$1*; do
		enstring="$enstring -settype xydy $filename"
	done
	xmgrace $enstring -nosafe -noask -legend load -pexec 'xaxis label "Temp"' -pexec 'yaxis label "Energy"' &

	#Magsquare
	magstring="-param ../scripts/default.par"
	for filename in ./foutput/m2/*$1*; do
		magstring="$magstring -settype xydy $filename"
	done
	xmgrace $magstring -nosafe -noask -legend load -pexec 'xaxis label "Temp"' -pexec 'yaxis label "Magnetization^2"' &


	#Magquart
	dbdtstring="-param ../scripts/default.par"
	for filename in ./foutput/m4/*$1*; do
		dbdtstring="$dbdtstring -settype xydy $filename"
	done
	xmgrace $dbdtstring -nosafe -noask -legend load -pexec 'xaxis label "Temp"' -pexec 'yaxis label "Magnetization^4"' &
	#Susceptibility
	xistring="-param ../scripts/default.par"
	for filename in ./foutput/xi/*$1*; do
		xistring="$xistring -settype xydy $filename"
	done
	xmgrace $xistring -nosafe -noask -legend load -pexec 'xaxis label "Temp"' -pexec 'yaxis label "Susceptibility"' &
fi

