import subprocess
import sys
nruns = sys.argv[1]
fname = sys.argv[2]
rtype =sys.argv[3]
L = sys.argv[4]
sT = sys.argv[5]
eT = sys.argv[6]
nT = sys.argv[7]
Neq = sys.argv[8]
Nsamp = sys.argv[9]
cold = sys.argv[10]
fname=str(fname)
rtype=str(rtype)
L=str(L)
sT=str(sT)
eT=str(eT)
nT=str(nT)
Neq=str(Neq)
Nsamp=str(Nsamp)
cold=str(cold)
rtype += " "
L += " "
sT += " "
eT += " "
nT += " "
Neq += " "
Nsamp += " "
cold += " "
for i in range(int(nruns)):
    runfile = open("run","w")
    oname = "output/" + str(fname) + str(i);
    runfile.write("#!/bin/bash\n./main.exe " + rtype + L + sT +eT + nT +Neq + Nsamp+cold + oname) 
    runfile.close()
    subprocess.call(["cat","run"])
