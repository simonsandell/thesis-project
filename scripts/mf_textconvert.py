import numpy as np
import sys
import os
from multiprocessing import Pool

import textToFloats


u= "_";

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
        lval = np.unique(ret[:,0]);
        tval = np.unique(ret[:,1]);
        str_i = "";
        for l in lval:
            str_i += str(l)+u;
        tmax = str(tval.max());
        tmin = str(tval.min());
        str_i += tmax+u+tmin+u;
        np.save("./pickles/"+model+u+filename+u+str_i,ret);

pool = Pool(processes=4,maxtasksperchild=1);
poolres= pool.map(func,filenames);
pool.close()
pool.join()

print(timeit.default_timer() - inittime)
