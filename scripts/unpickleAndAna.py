from multiprocessing import Pool
import numpy as np
import pandas as pd
import sys
import time

import fileWriter
import pickler



fName = sys.argv[1];
model = sys.argv[2];

data = pickler.loadData(model+fName);

def calcForOneLOneT(index):
    view = data[index[0]:index[1],:];
    avg = [];
    for i in range(view.shape[1]):
        avg.append(np.mean(view[:,i]));
    avg.extend(view.shape[0]);
    return avg;

# find indices
args = [];
Lv,Li = np.unique(data[:,ind.L],return_index=True);
Li = np.append(Li,data.shape[0]);
for l1,l2 in zip(Li[:-1],Li[1:]):
    Tv,Ti = np.unique(data[l1:l2,ind.T],return_index=True);
    Ti = np.append(Ti,(l2-l1));
    for t1,t2 in zip(Ti[:-1],Ti[1:]):
        args.append(((l1+t1),(l1+t2)));
res = []
pool = Pool(processes=6);
res.append(pool.map(calcForOneLOneT,args));
pool.close()
pool.join()
print(time.process_time());
res = np.array(res);
res = res.squeeze();
print(res.shape)

fileWriter.writeDataTable(fName,model,res);
