#!/bin/bash
#regular temperature plot
directory=$1
xaxis=$2
yaxis="$(basename $directory)"
string="-param ../scripts/default.par"
for filename in $directory*; do
	string="$string -settype xydy $filename"
done
xmgrace $string -pexec "xaxis label \"$xaxis\"" -pexec "yaxis label \"$yaxis\"" -nosafe -noask -free -legend load &

