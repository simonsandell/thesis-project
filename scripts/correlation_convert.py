import os
import numpy as np
import settings
from datahandle import textToFloats

d = settings.root_path + "modular/output/3DXY/correlation/"
dirlist = [
    d + "4/",
    d + "8/",
    d + "16/",
    d + "32/",
    d + "64/",
    d + "128/",
]
n_vals = 6
datlist = []
for l_idx, direc in enumerate(dirlist):
    datlist = np.empty((0, n_vals))
    for fname in os.listdir(direc):
        if "jul_24" in fname:
            print(os.path.join(direc, fname))
            datlist = np.append(datlist, np.array(textToFloats.loadData(os.path.join(direc, fname), n_vals)), axis=0)
    np.save(settings.pickles_path + "correlation/" + settings.TAG + repr(4*pow(2, l_idx)), datlist)


