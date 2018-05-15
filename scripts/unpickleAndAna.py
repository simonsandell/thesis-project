from multiprocessing import Pool
import numpy as np
import sys
import time
import math

import jackknife
import fileWriter
import modelAvgs as ma
#import pickler



fName = sys.argv[1];
model = sys.argv[2];

#data = pickler.loadData(model+fName);
data = np.load("./pickles/"+model+fName+".npy");
def modelAvgs(avgs,mod=model):
    res = np.zeros(5);
    if (mod == "3DXY"):
        res[0] = ma.getBin(avgs[10],avgs[11],avgs[21])
        res[1] = ma.getdBdT(avgs[10],avgs[11],avgs[12],avgs[13],avgs[7],avgs[21],avgs[1],math.pow(avgs[0],3));
        res[2] = ma.getRs(avgs[7],avgs[14],avgs[15],avgs[16],avgs[21],avgs[0],avgs[1]);
        res[3] = ma.getChi(avgs[9],avgs[10],avgs[21],avgs[1],math.pow(avgs[0],3));
        res[4] = ma.getC(avgs[7],avgs[8],avgs[21],avgs[1],math.pow(avgs[0],3));
    return res;

def avgF(x):
    res = np.zeros(x.shape[1]);
    for i in range(x.shape[1]):
        res[i]= (np.mean(x[:,i]));
    modavgs = modelAvgs(res);
    res = np.append(res,modavgs);
    return res;

def calcForOneLOneT(view):
    avg = avgF(view);
    j_est = jackknife.jackknife(view,avgF,avg.shape[0]);
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

