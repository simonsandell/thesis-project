import numpy as np
import os
import sys
from plotting import fileWriter
import settings

def getIntersections(view):
    res = np.empty((0,view.shape[1])); 
    for x in range(view.shape[0]):
        if not (np.isnan(view[x,1])):
            res=np.append(res,[view[x,:]],axis=0);
    return res;

def getCloseness(ints):
    avgx = np.mean(ints[:,1]);
    avgy = np.mean(ints[:,2]);
    o = np.ones(ints[:,0].shape);
    dx = ints[:,1] - o*avgx;
    dy = ints[:,2] - o*avgx;
    dist = np.float_power(dx,o*2) + np.float_power(dy,o*2);
    res = np.mean(dist);
    return res;

# format;
# omega, int_x, int_y, L1, L2
#     0     1     2   3   4
# takes a group of intersectionfiles and compares closeness for each value of omega,
# then prints to file in foutput/model/vsO/
def twoLintersectionCloseness(dat,model,savename):
    dat = dat[dat[:,0].argsort()];
    
    ov,oi = np.unique(dat[:,0],return_index=True);
    oi = np.append(oi,dat.shape[0]);
    
    result = [];
    for i,(i1,i2) in enumerate(zip(oi[:-1],oi[1:])):
        omview = dat[i1:i2,:];
        ints = getIntersections(omview);
    
        if (ints.shape[0]>2):
            closeness = getCloseness(ints);
            result.append([ov[i],closeness,0.0]);
    np.save(settings.pickles_path+savename,result);
    fileWriter.writeOmegaVsClose(savename,model,result);
    
    
