import sys
import os
from _3DXY import analyze3DXY as anaT
from _3DXY import L_analyze3DXY as anaL
from _3DXY import scalCorr3DXY as anaSC
from _3DXY import rhos_omega as anaRS
import numpy as np

arguments = sys.argv;
fName = arguments[1];
datafile = open("./output/3DXY/"+fName,"r");
data = [];
for ln in datafile:
    strlist = ln.rsplit(" ");
    strlist = [x for x in strlist if not (x== "\n")];
    fllist = [float(x) for x in strlist];
    data.append(fllist);
dataMatrix = np.array(data);
print("loading done, starting t data");
#anaT.analyze(dataMatrix,fName);
print("temp data done,starting l data");
#anaL.analyze(dataMatrix,fName);
print("L data done, staring scaling corrections");
#anaSC.analyze(dataMatrix,fName);
print("scaling corr done, starting rho_s_omega");
anaRS.analyze(dataMatrix,fName);
print("analysis done");
