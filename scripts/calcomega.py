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
o1file = open("./foutput/omega/omega1.dat","a")
o2file = open("./foutput/omega/omega2.dat","a")
o3file = open("./foutput/omega/omega3.dat","a")
o4file = open("./foutput/omega/omega4.dat","a")
flist = [o1file,o2file,o3file,o4file];
fstr= "{:30.30f}";
for x in range((len(vals) -2 )):

    bdiff = vals[x+1][1] - vals[x+0][1];
    bdiff2 = vals[x+2][1] - vals[x+1][1];
    bdiv = bdiff2/bdiff
    omega = -math.log(bdiv)/math.log(2)
    flist[x].write(fstr.format(T) + "    " +fstr.format(omega) + "    " +fstr.format(0.0) + "    " + fstr.format(vals[0][3]) + "    \n")

