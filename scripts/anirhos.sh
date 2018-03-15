#!/bin/bash
filedir=$1
animationfile="./foutput/animations/$(basename $filedir).gif"
pngdir=$1_png
rm -r $pngdir
mkdir $pngdir 
echo $filedir
echo $animationfile
echo $pngdir
for subdir in $filedir/*/; do
	string="-legend load";
	omega=""
	for file in $subdir*.dat; do
		if [ -z "$omega" ]; then
	      		omega=$(head -n 1 $file | awk -F' ' '{ print $4 }' )
		fi
		string="$string -settype xydy $file"
	done
	echo $string
	rm ../scripts/setup.batch
	echo "XAXIS LABEL \"Temperature\" " > ../scripts/setup.batch
	echo "YAXIS LABEL \"L\S\xw\0\N\c7\C[2L\c7\C\xr\0\ss\N(2L) - \L\c7\C\xr\0\ss\N(L)]\" " >> ../scripts/setup.batch
	echo "YAXIS TICK MAJOR 0.05 " >> ../scripts/setup.batch
	echo "YAXIS TICK MINOR 0.025 " >> ../scripts/setup.batch
	echo "TITLE \"\xw = $omega\" " >> ../scripts/setup.batch
	echo "AUTOSCALE ONREAD NONE" >> ../scripts/setup.batch
	echo "WORLD XMIN 2.2015 " >> ../scripts/setup.batch #read these from file?
	echo "WORLD XMAX 2.203" >> ../scripts/setup.batch
	echo "WORLD YMIN -0.025" >> ../scripts/setup.batch
	echo "WORLD YMAX 0.15" >> ../scripts/setup.batch
	echo "LEGEND ON " >> ../scripts/setup.batch
	echo "LEGEND LOCTYPE WORLD" >> ../scripts/setup.batch
	echo "LEGEND 2.202, 0.14 " >> ../scripts/setup.batch
	gracebat -batch ../scripts/setup.batch $string  -nosafe -printfile $pngdir/$(basename $subdir).png -hdevice PNG -hardcopy  
done
convert -delay 50 $pngdir/*.png $animationfile
eog $animationfile
