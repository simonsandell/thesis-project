import numpy as np
import sys
import os
import timeit
from multiprocessing import Pool

import textToFloats

inittime = timeit.default_timer();



dirpath = sys.argv[1];
model = sys.argv[2];
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
        ret = np.array(ret);
        ret = ret.squeeze();
        ind = np.lexsort((ret[:,1],ret[:,0]));
        ret = ret[ind];
        path = textToFloats.getSavepath(ret,model,filename);
        np.save(path,ret);

pool = Pool(processes=1,maxtasksperchild=1);
poolres= pool.map(func,filenames);
pool.close()
pool.join()

print(timeit.default_timer() - inittime)
