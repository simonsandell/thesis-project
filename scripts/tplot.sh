#!/bin/bash
#Display a selection of plots from the output of analyzeData.py using xmgrace -free

#Only plot rest if requested
if [ ! $# -eq 0 ]
then
	#Binder paramter
	binstring="-param ../scripts/default.par"
	for filename in ./foutput/$1/bin/*$2*; do
		binstring="$binstring -settype xydy $filename"
	done
	xmgrace -free $binstring -nosafe -noask -legend load -pexec 'xaxis label "Temp"' -pexec 'yaxis label "Binder Cumulant"' &
	
	#Superfluid density
	rsstring="-param ../scripts/default.par"
	for filename in ./foutput/$1/rs/*$2*; do
		rsstring="$rsstring -settype xydy $filename"
	done
	xmgrace -free $rsstring -nosafe -noask -legend load -pexec 'xaxis label "Temp"' -pexec 'yaxis label "Superfluid density"' &
	
	#Energy per spin
	enstring="-param ../scripts/default.par"
	for filename in ./foutput/$1/en/*$2*; do
		enstring="$enstring -settype xydy $filename"
	done
	xmgrace -free $enstring -nosafe -noask -legend load -pexec 'xaxis label "Temp"' -pexec 'yaxis label "Energy"' &

	#Magnetization per spin
	magstring="-param ../scripts/default.par"
	for filename in ./foutput/$1/mag/*$2*; do
		magstring="$magstring -settype xydy $filename"
	done
	xmgrace -free $magstring -nosafe -noask -legend load -pexec 'xaxis label "Temp"' -pexec 'yaxis label "Magnetization"' &


	#dB/dT
	dbdtstring="-param ../scripts/default.par"
	for filename in ./foutput/$1/dbdt/*$2*; do
		dbdtstring="$dbdtstring -settype xydy $filename"
	done
	xmgrace -free $dbdtstring -nosafe -noask -legend load -pexec 'xaxis label "Temp"' -pexec 'yaxis label "dB/dT"' &
	#Susceptibility
	xistring="-param ../scripts/default.par"
	for filename in ./foutput/$1/xi/*$2*; do
		xistring="$xistring -settype xydy $filename"
	done
	xmgrace -free $xistring -nosafe -noask -legend load -pexec 'xaxis label "Temp"' -pexec 'yaxis label "Susceptibility"' &
fi

