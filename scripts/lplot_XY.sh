#!/bin/bash
#Display a selection of plots from the output of analyzeData.py using xmgrace -free

if [ ! $# -eq 0 ]
then
	#Binder paramter
	binstring="-param ../scripts/default.par"
	for filename in ./foutput/3DXY/L_bin/*$2*; do
		binstring="$binstring -settype xydy $filename"
	done
	xmgrace -free $binstring -log x -log y -nosafe -noask -legend load -pexec 'xaxis label "L"' -pexec 'yaxis label "Binder Cumulant"' &
	
	#Superfluid density
	rsstring="-param ../scripts/default.par"
	for filename in ./foutput/3DXY/L_rs/*$2*; do
		rsstring="$rsstring -settype xydy $filename"
	done
	xmgrace -free $rsstring -log x -log y -nosafe -noask -legend load -pexec 'xaxis label "L"' -pexec 'yaxis label "Superfluid density"' &
	
	#Energy per spin
	enstring="-param ../scripts/default.par"
	for filename in ./foutput/3DXY/L_en/*$2*; do
		enstring="$enstring -settype xydy $filename"
	done
	xmgrace -free $enstring -log x -log y -nosafe -noask -legend load -pexec 'xaxis label "L"' -pexec 'yaxis label "Energy"' &

	#Magnetization per spin
	magstring="-param ../scripts/default.par"
	for filename in ./foutput/3DXY/L_mag/*$2*; do
		magstring="$magstring -settype xydy $filename"
	done
	xmgrace -free $magstring -log x -log y -nosafe -noask -legend load -pexec 'xaxis label "L"' -pexec 'yaxis label "Magnetization"' &


	#dB/dT
	dbdtstring="-param ../scripts/default.par"
	for filename in ./foutput/3DXY/L_dbdt/*$2*; do
		dbdtstring="$dbdtstring -settype xydy $filename"
	done
	xmgrace -free $dbdtstring -log x -log y -nosafe -noask -legend load -pexec 'xaxis label "L"' -pexec 'yaxis label "dB/dT"' &
	#Susceptibility
	xistring="-param ../scripts/default.par"
	for filename in ./foutput/3DXY/L_xi/*$2*; do
		xistring="$xistring -settype xydy $filename"
	done
	xmgrace -free $xistring -log x -log y -nosafe -noask -legend load -pexec 'xaxis label "L"' -pexec 'yaxis label "Susceptibility"' &
fi

