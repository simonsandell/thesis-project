import time
import sys
import math
import numpy as np
import settings
import testIntersection
#import matplotlib.pyplot as plt
#import matplotlib.animation as animation


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
    if len(bres)==0:
        bres = [np.nan,np.nan];
    if len(rres)==0:
        rres = [np.nan,np.nan];
    return [bres,rres];

def rescaleQuants(dat,omega):
    res = np.copy(dat);
    for i in range(dat.shape[0]):
        res[i,3] = dat[i,3]*np.float_power(dat[i,0],omega);
        res[i,4] = dat[i,4]*np.float_power(dat[i,0],omega);
        res[i,7] = dat[i,7]*np.float_power(dat[i,0],omega);
        res[i,8] = dat[i,8]*np.float_power(dat[i,0],omega);
    return res;

# takes two datafiles of datafiles and finds their intersecions, saves to npy file in pickles
# 

def twoLfindIntersection(dat1,dat2,model):
    global bresult;
    global rresult;
    #format : L, L2, T, Bin_q, Rs_q, NL, NL2, dB, dR
    #         0   1  2  3      4     5   6    7   8
    L1 = dat1[0,0];
    L2 = dat2[0,0];
    omega_start = 0;
    omega_end = 2;
    omega_step = 0.01;
    
    # save frames for animation
    bin_values_1 = []
    bin_values_2 = []
    
    # could parrallellize here
    bresult =[];
    rresult =[];
    omega_range = np.arange(omega_start,omega_end,omega_step);
    N_omegas = len(omega_range);
    
    #fig =plt.figure();
    #ax = plt.axes(xlim =(2.2016,2.202),ylim=(0,0.4));
    #line, = ax.plot([],[],lw=2);
    #plt.xlabel('temperature')
    #plt.ylabel('L^omega * (B(2L) - B(l))');
    #plotlays,plotcols = [2],["black","red"];
    
    #lines = [];
    #for ind in range(2):
    #    lobj = ax.plot([],[],lw=2,color=plotcols[ind])[0];
    #    lines.append(lobj);
    #
    #def init():
    #    for line in lines:
    #        line.set_data([],[]);
    #    return lines;
        
    def update(i):
        global bresult;
        global rresult;
        omega = omega_range[i];
        rdat1 =rescaleQuants(dat1,omega);
        rdat2 =rescaleQuants(dat2,omega);
        intersections = findIntersections(rdat1,rdat2);
        bint = intersections[0];
        rint = intersections[1];
        if not np.isnan(bint[0]):
            bresult.append([omega,bint[0],bint[1],L1,L2])
        if not np.isnan(rint[0]):
            rresult.append([omega,rint[0],rint[1],L1,L2])
        #xdata = rdat1[:,2]
        #ylist = [rdat1[:,4],rdat2[:,4]];
        #for lnum,line in enumerate(lines):
        #    line.set_data(xdata,ylist[lnum]);
        #return lines
    doAnim = "no"
    if doAnim =="y":
        pass
        #anim = animation.FuncAnimation(fig,update,init_func=init,frames=N_omegas);
        #plt.show()
    else:
        for i in range(N_omegas):
            update(i);
    bresult = np.array(bresult);
    rresult = np.array(bresult);
    np.save(settings.pickles_path+"2LomegaIntBin"+str(L1)+"_"+str(L2),bresult);
    np.save(settings.pickles_path+"2LomegaIntRho"+str(L1)+"_"+str(L2),rresult);
    return [bresult,rresult];
