import sys
import os
import numpy as np

import textToFloats

path = sys.argv[1];
model = sys.argv[2];
if model == "3DXY":
    nvals = 22;

fNames = "";
mixedmat = np.empty((0,nvals));
for filename in os.listdir(path):
    fNames+=filename+"_";
    data = np.load(os.path.join(path,filename));
    mixedmat = np.append(mixedmat,data,axis=0);

ind = np.lexsort((mixedmat[:,1],mixedmat[:,0]));
mixedmat = mixedmat[ind];
lval,lind = np.unique(mixedmat[:,0],return_index=True);
lind = np.append(lind,mixedmat.shape[0]);
for i in range(lind.shape[0]-1):
    view = mixedmat[lind[i]:lind[i+1],:];
    np.save(textToFloats.getSavepath(view,model,fNames),view);

