import os
import timeit
import sys
import numpy as np
from multiprocessing import Pool

import textToFloats
inittime = timeit.default_timer();


dirpath = sys.argv[1];
model = sys.argv[2];
saveName = sys.argv[3];
if (sys.argv[2] == "3DXY"):
    nvals = 22;
else:
    nvals = 19;

poolres = [];
res = [];
filenames = sorted(os.listdir(dirpath));
N_files = len(filenames);
def func(filename):
    print(filename)
    if (os.path.isfile(os.path.join(dirpath,filename))):
        ret = textToFloats.loadData(os.path.join(dirpath,filename),nvals);
        return ret;
pool = Pool(processes=4,maxtasksperchild=1);
poolres= pool.map(func,filenames);
pool.close()
pool.join()
for x in poolres:
    print(len(x))
    res.extend(x);
npmat = np.array(res);
npmat = npmat.squeeze();
print(npmat.shape)
print(npmat[0]);
ind = np.lexsort((npmat[:,1],npmat[:,0]));

npmat = npmat[ind];
print(npmat.shape);
lval = np.unique(npmat[:,0]);
u="_";
for v in lval:
    strL += str(v)+u;
tval = np.unique(npmat[:,1]);
tmax = np.max(tval);
tmin = np.min(tval);
strL += str(tmin)+"-"+str(tmax);

np.save("./pickles/"+model+saveName+u+strL,npmat);
print(timeit.default_timer() - inittime)
