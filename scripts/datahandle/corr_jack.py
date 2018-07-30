import os
import numpy as np

import settings
for f in os.listdir(settings.pickles_path + "correlation/"):
    if "jul_26_final" in f:
        arr = np.load(os.path.join(settings.pickles_path+"correlation/", f))
        jval = np.unique(arr[:, -1])
        jnum = jval.shape[0]
        tempnum = int(arr.shape[0]/jnum)
        print(tempnum)
        print(int(tempnum))
        jarr = np.empty((jnum,tempnum, arr.shape[1]))
        for j in range(jnum):
            jarr[j, : , :] = arr[j*tempnum:(j+1)*tempnum, :]
        np.save(settings.pickles_path+"correlation/jack/jack_" + f.rstrip(".npy"),jarr)
        print(jarr.shape)





