#!/bin/bash
#Display a selection of plots from the output of analyzeData.py using xmgrace

#Only plot rest if requested
if [ ! $# -eq 0 ]
then
	#Binder paramter
	binstring="-param ../scripts/default.par"
	for filename in ./foutput/Ising3D/bin/*$1*; do
		binstring="$binstring -settype xydy $filename"
	done
	xmgrace -free $binstring -nosafe -noask -legend load -pexec 'xaxis label "Temp"' -pexec 'yaxis label "Binder Cumulant"' &
	
	#heatcap
	rsstring="-param ../scripts/default.par"
	for filename in ./foutput/Ising3D/c/*$1*; do
		rsstring="$rsstring -settype xydy $filename"
	done
	xmgrace -free $rsstring -nosafe -noask -legend load -pexec 'xaxis label "Temp"' -pexec 'yaxis label "Heat capacity"' &
	
	#Energy per spin
	enstring="-param ../scripts/default.par"
	for filename in ./foutput/Ising3D/en/*$1*; do
		enstring="$enstring -settype xydy $filename"
	done
	xmgrace -free $enstring -nosafe -noask -legend load -pexec 'xaxis label "Temp"' -pexec 'yaxis label "Energy"' &

	#Magsquare
	magstring="-param ../scripts/default.par"
	for filename in ./foutput/Ising3D/m2/*$1*; do
		magstring="$magstring -settype xydy $filename"
	done
	xmgrace -free $magstring -nosafe -noask -legend load -pexec 'xaxis label "Temp"' -pexec 'yaxis label "Magnetization^2"' &


	#Magquart
	dbdtstring="-param ../scripts/default.par"
	for filename in ./foutput/Ising3D/m4/*$1*; do
		dbdtstring="$dbdtstring -settype xydy $filename"
	done
	xmgrace -free $dbdtstring -nosafe -noask -legend load -pexec 'xaxis label "Temp"' -pexec 'yaxis label "Magnetization^4"' &
	#Susceptibility
	xistring="-param ../scripts/default.par"
	for filename in ./foutput/Ising3D/xi/*$1*; do
		xistring="$xistring -settype xydy $filename"
	done
	xmgrace -free $xistring -nosafe -noask -legend load -pexec 'xaxis label "Temp"' -pexec 'yaxis label "Susceptibility"' &
fi

