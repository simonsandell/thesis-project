import sys
import math

fName = sys.argv[1]

dat = open(fName,"r")
vals = []
nL = 0
for ln in dat:
    row= ln.rsplit(" ");
    row= [x for x in row if not (x=="\n")]
    row= [x for x in row if not (x=="")]
    row= [x.replace('\n','') for x in row]
    frow= [float(x) for x in row] 
    vals.append(frow);
    nL = nL +1;

T = vals[0][4];
fnfstr = "{:8.8f}"
ofile = open("./foutput/omega/omega.dat","a")
fstr= "{:30.30f}";
bdiff = vals[1][1] - vals[0][1];
bdiff2 = vals[2][1] - vals[1][1];
bdiv = bdiff2/bdiff
omega = -math.log(bdiv)/math.log(2)
ofile.write(fstr.format(T) + "    " +fstr.format(omega) + "    " +fstr.format(0.0) + "    " + fstr.format(vals[0][3]) + "    \n")

