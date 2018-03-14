#!/bin/bash
rm ./foutput/3DXY/rho_s_png/*
for dir in ./foutput/3DXY/rhos_omega/*/; do
	string="";
	omega=""
	for file in $dir*; do
		if [ -z "$omega" ]; then
	      		omega=$(head -n 1 $file | awk -F' ' '{ print $4 }' )
		fi
		string="$string -settype xydy $file"
	done
	rm ../scripts/setup.batch
	echo "XAXIS LABEL \"Temperature, \xw = $omega\"" > ../scripts/setup.batch
	echo "YAXIS LABEL \"\xr\0\ss\N\c7\CL\S1-\xw\N\"" >> ../scripts/setup.batch
	gracebat $string -batch ../scripts/setup.batch -autoscale xy -nosafe -printfile ./foutput/3DXY/rho_s_png/$(basename $dir).png -hdevice PNG -hardcopy  
done

convert -delay 100 ./foutput/3DXY/rho_s_png/*.png ./animation.gif
eog animation.gif
