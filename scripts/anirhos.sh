#!/bin/bash
rm ./foutput/3DXY/rho_s_png/*
for dir in ./foutput/3DXY/rhos_omega/*/; do
	string="-legend load";
	omega=""
	for file in $dir*; do
		if [ -z "$omega" ]; then
	      		omega=$(head -n 1 $file | awk -F' ' '{ print $4 }' )
		fi
		string="$string -settype xydy $file"
	done
	rm ../scripts/setup.batch
	echo "XAXIS LABEL \"Temperature\" " > ../scripts/setup.batch
	echo "YAXIS LABEL \"\xr\0\ss\N\c7\CL\S1-\xw\N\" " >> ../scripts/setup.batch
	echo "TITLE \"\xw = $omega\" " >> ../scripts/setup.batch
	echo "AUTOSCALE ONREAD NONE" >> ../scripts/setup.batch
	echo "WORLD XMIN 2.2015 " >> ../scripts/setup.batch #read these from file?
	echo "WORLD XMAX 2.203" >> ../scripts/setup.batch
	echo "WORLD YMIN -0.05" >> ../scripts/setup.batch
	echo "WORLD YMAX 0.15" >> ../scripts/setup.batch
	echo "LEGEND ON " >> ../scripts/setup.batch
	echo "LEGEND LOCTYPE WORLD" >> ../scripts/setup.batch
	echo "LEGEND 2.202, 0.14 " >> ../scripts/setup.batch
	gracebat -batch ../scripts/setup.batch $string  -nosafe -printfile ./foutput/3DXY/rho_s_png/$(basename $dir).png -hdevice PNG -hardcopy  
done

convert -delay 10 ./foutput/3DXY/rho_s_png/*.png ./animation.gif
eog animation.gif
