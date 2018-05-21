import numpy as np
import pickle

from _3DXY import analyze3DXY as ana
f_vsT =ana.calc_vsT ;
def doForRanges(idx,do):
    for i1,i2 in zip(idx[:-1],idx[1:]):
        do(i1,i2);
    

with open("../modular/pickles/short_T_32.pickle","rb") as f:
    rawdata = pickle.load(f);
print("done unpickling")
print(rawdata.shape)
ind = np.lexsort((rawdata[:,1],rawdata[:,0]));
print("done sorting");
data = rawdata[ind];
print(ind.shape)
print(data.shape)
print("done sorting");
tv,ti = np.unique(data[:,1],return_index=True)
ti = np.append(ti,data.shape[0])
print(ti)
minires = f_vsT(data[ti[0]:ti[1],:]);
print(minires)
#res = doForRanges(ti,lambda x,y:f_vsT(data[x:y,:]));
