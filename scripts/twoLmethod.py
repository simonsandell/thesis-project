from analysis import twoLana
from analysis import twoLomega
from analysis import twoLomegaVsGood
import sys
import settings
import numpy as np



savename = input("savename: ");
model = settings.model;

datafiles = [
settings.pickles_path+"4combined_reduced.npy",
settings.pickles_path+"8combined_reduced.npy",
settings.pickles_path+"16combined_reduced.npy",
settings.pickles_path+"32combined_reduced.npy",
settings.pickles_path+"64combined_reduced.npy",
settings.pickles_path+"128combined_reduced.npy"];

# calculate the quantities, plain
twoLquant = []
for data1,data2 in zip(datafiles[:-1],datafiles[1:]):
    twoLquant.append(twoLana.twoLomega(np.load(data1),np.load(data2),model,savename));


# for range of omega, rescale and find intersection between sequentially larger system sizes
bres,rres = np.empty((0,5)),np.empty((0,5));
for q1,q2 in zip(twoLquant[:-1],twoLquant[1:]):
    bothres = twoLomega.twoLfindIntersection(q1,q2,model);
    bres=np.append(bres,bothres[0],axis=0);
    rres=np.append(rres,bothres[1],axis=0);
# result format:
# bres = [[omega,intx,inty,L1,L2],...]

# calculate how close intersections are for each omega and save to xmgrace file
twoLomegaVsGood.twoLintersectionCloseness(bres,"bin",savename+"bind_good");
twoLomegaVsGood.twoLintersectionCloseness(rres,"rs",savename+"rho_good");
# skipping smallest, do it again
bres_ds = twoLomega.removeSmallestSize(bres);
rres_ds = twoLomega.removeSmallestSize(rres);
twoLomegaVsGood.twoLintersectionCloseness(bres_ds,"bin",savename+"_ds_bind_good");
twoLomegaVsGood.twoLintersectionCloseness(rres_ds,"rs",savename+"_ds_rho_good");



