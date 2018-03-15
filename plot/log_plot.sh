#!/bin/bash
#Display a selection of plots from the output of analyzeData.py using xmgrace -free
directory=$1
yaxis="$(basename $directory)"
xaxis=$2

string="-param ../scripts/default.par"	
for filename in directory/*; do
	string="$string -settype xydy $filename"
done
	xmgrace -free $string -log x -log y -nosafe -noask -legend load -pexec "xaxis label \"$xaxis\"" -pexec "yaxis label \"$yaxis\"" &
