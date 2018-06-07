import numpy as np
import os
import settings
from multiprocessing import Pool

from datahandle import textToFloats

dirpath = input("convert files in: " + settings.root_path)
dirpath = settings.root_path + dirpath
model = settings.model
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
        ret = np.array(ret)
        ret = ret.squeeze()
        ind = np.lexsort((ret[:, 1], ret[:, 0]))
        ret = ret[ind]
        np.save(os.path.join(dirpath, filename), ret)


pool = Pool(processes=1, maxtasksperchild=1)
poolres = pool.map(func, filenames)
pool.close()
pool.join()
