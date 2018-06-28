import os
import timeit
import sys
import numpy as np
import settings
from multiprocessing import Pool

from datahandle import textToFloats

inittime = timeit.default_timer()

# parallell script, loads all files in dir and converts to npy
# saves in settings.picklepath
dirpath = sys.argv[1]
model = settings.model
saveName = sys.argv[2]

if model == "3DXY":
    nvals = 22
else:
    nvals = 19

poolres = []
res = []
filenames = sorted(os.listdir(dirpath))
N_files = len(filenames)


def func(filename):
    print(filename)
    if os.path.isfile(os.path.join(dirpath, filename)):
        ret = textToFloats.loadData(os.path.join(dirpath, filename), nvals)
        return ret


pool = Pool(processes=4, maxtasksperchild=1)
poolres = pool.map(func, filenames)
pool.close()
pool.join()

for x in poolres:
    print(len(x))
    res.extend(x)
npmat = np.array(res)
npmat = npmat.squeeze()
print(npmat.shape)
print(npmat[0])
ind = np.lexsort((npmat[:, 1], npmat[:, 0]))

npmat = npmat[ind]
print(npmat.shape)
lval = np.unique(npmat[:, 0])
u = "_"
strL = ""

for v in lval:
    strL += str(v) + u
tval = np.unique(npmat[:, 1])
tmax = np.max(tval)
tmin = np.min(tval)
strL += str(tmin) + "-" + str(tmax)

np.save(settings.pickles_path + model + saveName + u + strL, npmat)
