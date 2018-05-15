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

def calcForOneLOneT(view):
    avg = avgF(view);
    j_est = jackknife.jackknife(view,avgF);
    j_avg = np.mean(j_est,axis=0);
    j_std = np.std(j_est,axis=0);
    avg =np.append(avg,view.shape[0]);
    j_delta = j_std*np.sqrt(j_est.shape[0]-1);
    avg = np.append(avg,j_delta);
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
pool = Pool(processes=4);
res.append(pool.map(calcForOneLOneT,args));
pool.close()
pool.join()
res = np.array(res);
res = res.squeeze();
print(time.process_time());

fileWriter.writeDataTable(fName,model,res);
np.save("./pickles/datatable_"+fName+model,res);
#fileWriter.writeVsT(fName,model,res);

