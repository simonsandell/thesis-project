from twoLomega import twoLana,twoLomega,twoLomegaVsGood
import sys
import settings
import numpy as np


model = "3DXY"
savename = "ts";
datafiles = [settings.pickles_path+model+"ts_4.npy",
settings.pickles_path+model+"ts_8.npy",
settings.pickles_path+model+"ts_16.npy",
settings.pickles_path+model+"ts_32.npy",
settings.pickles_path+model+"ts_64.npy",
settings.pickles_path+model+"ts_128.npy"];

twoLquant = []
for data1,data2 in zip(datafiles[:-1],datafiles[1:]):
    twoLquant.append(twoLana.twoLomega(np.load(data1),np.load(data2),model,savename));
bres,rres = [],[];
for q1,q2 in zip(twoLquant[:-1],twoLquant[1:]):
    bothres = twoLomega.twoLfindIntersection(q1,q2,model);
    bres.append(bothres[0]);
    rres.append(bothres[1]);

twoLomegaVsGood.twoLintersectionCloseness(bres,model,"bind_good");
twoLomegaVsGood.twoLintersectionCloseness(rres,model,"rho_good");


