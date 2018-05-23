from analysis import twoLana,twoLomega,twoLomegaVsGood
import sys
import settings
import numpy as np



savename = input("savename: ");
model = input("model: ");

datafiles = [
settings.pickles_path+"4combined_reduced.npy",
settings.pickles_path+"8combined_reduced.npy",
settings.pickles_path+"16combined_reduced.npy",
settings.pickles_path+"32combined_reduced.npy",
settings.pickles_path+"64combined_reduced.npy",
settings.pickles_path+"128combined_reduced.npy"];

twoLquant = []
for data1,data2 in zip(datafiles[:-1],datafiles[1:]):
    twoLquant.append(twoLana.twoLomega(np.load(data1),np.load(data2),model,savename));
bres,rres = [],[];
for q1,q2 in zip(twoLquant[:-1],twoLquant[1:]):
    bothres = twoLomega.twoLfindIntersection(q1,q2,model);
    bres.append(bothres[0]);
    rres.append(bothres[1]);

twoLomegaVsGood.twoLintersectionCloseness(bres,model,savename+"bind_good");
twoLomegaVsGood.twoLintersectionCloseness(rres,model,savename+"rho_good");


