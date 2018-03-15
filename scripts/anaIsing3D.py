import sys
import os
from Ising3D import analyzeIsing3D as anaT
from Ising3D import L_analyzeIsing3D as anaL
from Ising3D import scalCorrI3D as anaSC
import numpy as np

arguments = sys.argv;
fName = arguments[1];
datafile = open("./output/Ising3D/"+fName,"r");
data = [];
for ln in datafile:
    strlist = ln.rsplit(" ");
    strlist = [x for x in strlist if not (x== "\n")];
    fllist = [float(x) for x in strlist];
    data.append(fllist);
dataMatrix = np.array(data);
print("import done, starting t data");
anaT.analyze(dataMatrix,fName);
print("temp data done,starting l data");
anaL.analyze(dataMatrix,fName);
print("L data done, staring scaling corrections");
anaSC.analyze(dataMatrix,fName);
print("analysis done");
