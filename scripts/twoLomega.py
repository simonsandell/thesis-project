import sys
import math
import numpy as np
import settings
import testIntersection
#format : L, L2, T, Bin_q, Rs_q, NL, NL2, dB, dR
#         0   1  2  3      4     5   6    7   8

def findIntersections(rdat1,rdat2):
    # returns two intersections
    # loop over sequential pairs of T, check if intersects
    # if no intersection is found, returns nan
    # if more than one intersection if found, first one is returned
    bres = [];
    rres = [];
    for i1,i2 in zip(range(0,rdat1.shape[0]-1),range(1,rdat1.shape[0])):
        p1= np.array([rdat1[i1,2], rdat1[i1,3]])
        p2= np.array([rdat1[i2,2], rdat1[i2,3]])
        q1= np.array([rdat2[i1,2], rdat2[i1,3]])
        q2= np.array([rdat2[i2,2], rdat2[i2,3]])
        intersection = testIntersection.seg_intersect(p1,p2,q1,q2);
        if ((intersection[0] >= rdat1[i1,2]) and (intersection[0] <= rdat1[i2,2])):
            if len(bres)==0:
                bres = intersection;
            else:
                print(intersection);
                print("bin: too many intersections found");
        p1= np.array([rdat1[i1,2], rdat1[i1,4]])
        p2= np.array([rdat1[i2,2], rdat1[i2,4]])
        q1= np.array([rdat2[i1,2], rdat2[i1,4]])
        q2= np.array([rdat2[i2,2], rdat2[i2,4]])
        intersection = testIntersection.seg_intersect(p1,p2,q1,q2);
        if ((intersection[0] >= rdat1[i1,2]) and (intersection[0] <= rdat1[i2,2])):
            if len(rres)==0:
                rres = intersection;
            else:
                print(intersection);
                print("rho: too many intersections found");
    return [bres,rres];

def rescaleQuants(dat,omega):
    res = np.copy(dat);
    for i in range(dat.shape[0]):
        res[i,3] = dat[i,3]*np.float_power(dat[i,0],omega);
        res[i,4] = dat[i,4]*np.float_power(dat[i,0],omega);
        res[i,7] = dat[i,7]*np.float_power(dat[i,0],omega);
        res[i,8] = dat[i,8]*np.float_power(dat[i,0],omega);
    if len(bres)==0:
        bres = [np.nan,np.nan];
    if len(rres)==0:
        rres = [np.nan,np.nan];
    return res;

file1 = sys.argv[1];
file2 = sys.argv[2];
model = sys.argv[3];

#format : L, L2, T, Bin_q, Rs_q, NL, NL2, dB, dR
#         0   1  2  3      4     5   6    7   8
dat1= np.load(file1);
L1 = dat1[0,0];

dat2= np.load(file2);
L2 = dat2[0,0];
omega_start = 0;
omega_end = 2;
omega_step = 0.01;

# could parrallellize here
bresult =[];
rresult =[];
for omega in np.linspace(omega_start,omega_end,omega_step):
    rdat1 =rescaleQuants(dat1,omega);
    rdat2 =rescaleQuants(dat2,omega);
    intersections = findIntersections(rdat1,rdat2);
    bint = intersections[0];
    rint = intersections[1];
    bresult.append([omega,bint[0],bint[1],L1,L2])
    rresult.append([omega,rint[0],rint[1],L1,L2])
np.save(settings.pickles_path+"2LomegaIntBin"+str(L1)+"_"+str(L2),bresult);
np.save(settings.pickles_path+"2LomegaIntRho"+str(L1)+"_"+str(L2),rresult);


