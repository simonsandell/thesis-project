import os
import time
import sys
import numpy as np
import pickler
from multiprocessing import Pool

# N_vals = 22 for 3DXY, 19 for Ising3D
def loadData(path,N_vals):
    data = [];
    datafile = open(path,"r");
    i = 0;
    for ln in datafile:
        i = i+1;
        if not (('#' in ln) or ('WORLD' in ln) or ('SEED' in ln) or ('aprun' in ln)):
            strlist = ln.rsplit(" ");
            strlist = [x for x in strlist if not (x== "\n")];
            try:
                fllist = [float(x) for x in strlist];
                if (len(fllist) != N_vals):
                    print(path)
                    print(len(strlist));
                    print('bad line at row ' + str(1 + i));
                data.append(fllist);
            except:
                print(path);
                print('bad line at row ' + str(1 + i));
    return data;

dirpath = sys.argv[1];
model = sys.argv[2];
collectionName = sys.argv[3];
if (sys.argv[2] == "3DXY"):
    nvals = 22;
else:
    nvals = 19;

poolres = [];
res = [];
filenames = sorted(os.listdir(path));
N_files = len(filenames);
I = 0;j
def func(filename):
    I +=1;
    print(str(I)+"/"+str(N_files))
    if (os.path.isfile(os.path.join(path,filename))):
        print(filename);
        ret = loadData(os.path.join(path,filename),nvals);
        print(len(ret));
        return ret;
pool = Pool(processes=3,maxtasksperchild=1);
poolres= pool.map(func,filenames);
pool.close()
pool.join()
for x in poolres:
    res.extend(x);
npmat = np.array(res);
npmat = npmat.squeeze();
ind = np.lexsort(npmat[:,1],npmat[:,0]);
npmat = npmat[ind];
print(npmat.shape);
np.save("./pickles/"+model+saveName,npmat);
print(time.process_time())
