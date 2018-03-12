import sys
import os
import analyze3DXY as anaT
import L_analyze3DXY as anaL
import scalingCorr
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
dataMatrix = np.mat(data);

anaT.analyze(dataMatrix,fName);
print("temp data done");
anaL.analyze(dataMatrix,fName);
print("L data done");
scalingCorr.analyze(dataMatrix,fName);
