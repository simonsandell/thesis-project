from multiprocessing import Pool
import numpy as np
import sys
import time

import jackknife
import fileWriter
#import pickler



fName = sys.argv[1];
model = sys.argv[2];

#data = pickler.loadData(model+fName);
data = np.load("./pickles/"+model+fName+".npy");
def avgF(x):
    res = np.zeros(x.shape[1]);
    for i in range(x.shape[1]):
        res[i]= (np.mean(x[:,i]));
    return res;
def stdF(x):
    res=[];
    for i in range(x.shape[1]):
        res.append(
def calcForOneLOneT(view):
    avg = avgF(view);
    javg = jackknife.jackknife(view,avgF);
    for 
    avg.append(view.shape[0]);
    return avg;

# find indices
args = [];
Lv,Li = np.unique(data[:,0],return_index=True);
Li = np.append(Li,data.shape[0]);
for l1,l2 in zip(Li[:-1],Li[1:]):
    Tv,Ti = np.unique(data[l1:l2,1],return_index=True);
    Ti = np.append(Ti,(l2-l1));
    for t1,t2 in zip(Ti[:-1],Ti[1:]):
        args.append(data[(l1+t1):(l1+t2),:]);
res = []
pool = Pool(processes=1);
res.append(pool.map(calcForOneLOneT,args));
pool.close()
pool.join()
res = np.array(res);
res = res.squeeze();
print(time.process_time());

fileWriter.writeDataTable(fName,model,res);
#fileWriter.writeVsT(fName,model,res);

