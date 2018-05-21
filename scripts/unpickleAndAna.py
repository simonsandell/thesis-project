from multiprocessing import Pool
import numpy as np
import sys
import os
import timeit
import math
import settings

import jackknife
import fileWriter
import modelAvgs as ma
#import pickler
inittime = timeit.default_timer();


filepath = sys.argv[1];
fName = os.path.basename(filepath).rstrip(".npy");
model = sys.argv[2];

#data = pickler.loadData(model+filepath);
data = np.load(filepath);
#sort data

ind= np.lexsort((data[:,1],data[:,0]));
data = data[ind];


def modelAvgs(avgs,mod=model):
    res = np.zeros(7);
    if (mod == "3DXY"):
        res[0] = ma.getBin(avgs[10],avgs[11],avgs[21])
        res[1] = ma.getC(avgs[7],avgs[8],avgs[21],avgs[1],math.pow(avgs[0],3));
        res[2] = ma.getChi(avgs[9],avgs[10],avgs[21],avgs[1],math.pow(avgs[0],3));
        res[3] = ma.getdBdT(avgs[10],avgs[11],avgs[12],avgs[13],avgs[7],avgs[21],avgs[1],math.pow(avgs[0],3));
        res[4] = ma.getRs(avgs[7],avgs[14],avgs[15],avgs[16],avgs[21],avgs[0],avgs[1]);
        res[5] = avgs[7]/avgs[21];
        res[6] = avgs[9]/avgs[21];
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
        print((t2-t1))
        args.append(data[(l1+t1):(l1+t2),:]);
print("unique T's: " + str(len(args)));
res = []
pool = Pool(processes=6);
res.append(pool.map(calcForOneLOneT,args));
pool.close()
pool.join()
res = np.array(res);
res = res.squeeze();
print(timeit.default_timer()-inittime);

fileWriter.writeDataTable(fName,model,res);
np.save(settings.pickles_path+"datatable_"+fName+model,res);
fileWriter.writeVsT(fName,model,res);#assumes only one systemsize
fileWriter.writeVsL(filepath,model,res);#assumes only one temp


