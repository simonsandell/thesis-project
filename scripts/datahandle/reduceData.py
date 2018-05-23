import numpy as np
import os

def reduce(path):
    for fn in sorted(os.listdir(path)):
        fp = os.path.join(path,fn);
        if os.path.isfile(fp):
            print(fp)
            dat = np.load(fp);
            print(dat.shape);
            np.random.shuffle(dat);
            n_rows = 101*500;
            red = dat[:n_rows,:];
            ind = np.lexsort((red[:,1],red[:,0]));
            red = red[ind];
            np.save(fp.rstrip(".npy")+"_reduced",red);

p = input("path: ");
reduce(p);
