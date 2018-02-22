
binstring="-param ../scripts/default.par"
for filename in ./foutput/tempL/*; do
	binstring="$binstring -settype xydy $filename"
done
xmgrace $binstring -nosafe -noask -legend load -pexec 'xaxis label "L"' -pexec 'yaxis label "binder/rho "' &

