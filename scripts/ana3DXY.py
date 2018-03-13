import sys
import os
import analyze3DXY as anaT
import L_analyze3DXY as anaL
import scalingCorr as anaSC
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
ind = np.lexsort((dataMatrix[:,21],dataMatrix[:,20],dataMatrix[:,19],dataMatrix[:,18],dataMatrix[:,17],dataMatrix[:,16],dataMatrix[:,15],dataMatrix[:,14],dataMatrix[:,13],dataMatrix[:,12],dataMatrix[:,11],dataMatrix[:,10],dataMatrix[:,9],dataMatrix[:,8],dataMatrix[:,7],dataMatrix[:,5],dataMatrix[:,4],dataMatrix[:,3],dataMatrix[:,2],dataMatrix[:,6],dataMatrix[:,1],dataMatrix[:,0]));
dataMatrix = dataMatrix[ind];
print("sorting done, starting t data");
anaT.analyze(dataMatrix,fName);
print("temp data done,starting l data");
anaL.analyze(dataMatrix,fName);
print("L data done, staring scaling corrections");
anaSC.analyze(dataMatrix,fName);
print("analysis done");
