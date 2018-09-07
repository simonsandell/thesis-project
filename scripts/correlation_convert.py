import os
import numpy as np
import settings
from datahandle import textToFloats

d = settings.root_path + "modular/output/3DXY/correlation/"

Lval = 64
dirlist = [
    d + str(Lval)+"/aug/",
    #d + "8/",
    #d + "16/",
    #d + "32/",
    #d + "64/",
    #d + "128/",
]
n_vals = 7
datlist = []
for l_idx, direc in enumerate(dirlist):
    datlist = np.empty((0, n_vals))
    for fname in sorted(os.listdir(direc)):
        if not "aug_25" in fname:
            print(os.path.join(direc, fname))
            datlist = np.append(datlist, np.array(textToFloats.loadData(os.path.join(direc, fname), n_vals)), axis=0)
    np.save(settings.pickles_path + "correlation/new_" + settings.TAG + str(Lval), datlist)


