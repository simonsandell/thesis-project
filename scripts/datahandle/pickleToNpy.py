import pickle
import numpy as np
import os

def convert(path):
    for fn in os.listdir(path):
        fp = os.path.join(path,fn);
        print(fp)
        if os.path.isfile(fp):
            data = pickle.load(open(fp,"rb"));
            np.save(fp.rstrip(".pickle"),data);

p = input("path: ");
convert(p);
