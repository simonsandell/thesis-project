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
print(dataMatrix.shape);
dataMatrix = np.squeeze(dataMatrix);
print(dataMatrix.shape);
ind = np.lexsort((dataMatrix[:,21],dataMatrix[:,20],dataMatrix[:,19],dataMatrix[:,18],dataMatrix[:,17],dataMatrix[:,16],dataMatrix[:,15],dataMatrix[:,14],dataMatrix[:,13],dataMatrix[:,12],dataMatrix[:,11],dataMatrix[:,10],dataMatrix[:,9],dataMatrix[:,8],dataMatrix[:,7],dataMatrix[:,5],dataMatrix[:,4],dataMatrix[:,3],dataMatrix[:,2],dataMatrix[:,6],dataMatrix[:,1],dataMatrix[:,0]));
dataMatrix= dataMatrix[ind];
           
anaT.analyze(dataMatrix,fName);
print("temp data done");
anaL.analyze(dataMatrix,fName);
print("L data done");
scalingCorr.analyze(dataMatrix,fName);
