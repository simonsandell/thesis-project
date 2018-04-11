
import jackknife

import numpy as np
import scipy as sp

#returns avg mag
def jfunc(mat):
    return [np.mean(mat[:,9])];

def writeLine(mat,avgN):
    avgM = jfunc(mat)[0];
    delM = jackknife.getJackDelta(mat,jfunc,100)[0];
    return [avgN,avgM,delM];

#now we have data for only interesting temp, separete N_sweeps and print
def oneTemp(mat,nfac):
    result =[];
    startI = 0;
    high_N=4.0*nfac;
    avgPrev = 0.0;
    avgCurr = 0.0;
    for i in range(mat.shape[0]):
        if (mat[i,4]>high_N):
            avgCurr = np.mean(mat[startI:i,4]);
            result.append(writeLine(mat[startI:i],0.5*(avgCurr + avgPrev)));
            avgPrev = avgCurr;
            high_N= high_N*2;
            startI = i;
    avgCurr = np.mean(mat[startI:,4]);
    result.append(writeLine(mat[startI:,:],0.5*(avgCurr + avgPrev)));
    return result;


#we have block data for one L, pick out interesting temp.
def oneSize(mat,temp,betanu,z):
    #first, rescale mag and N
    for i in range(mat.shape[0]):
        mat[i,4] = mat[i,4]*pow(mat[i,0],-z);
        mat[i,9] = mat[i,9]*pow(mat[i,0],-betanu);

    TOL = 0.000000005;
    for i in range(mat.shape[0]):
        if (abs(mat[i,1] - temp) < TOL):
            startI = i;
            endI = i;
            while True:
                if (abs(mat[endI,1] - temp)< TOL):
                    endI = endI +1;
                else:
                    break;
                if (endI == mat.shape[0]):
                    break;
            break;
    ret = oneTemp(mat[startI:endI,:],pow(mat[i,0],-z));
    return ret;

#sort by L, then NTotSweeps
def analyze(mat,temp,betanu,z):
    ind = np.lexsort((mat[:,4],mat[:,1],mat[:,0]));
    smat = mat[ind];

    curr_L = mat[0,0];
    startI = 0;

    ret = [];
    for i in range(smat.shape[0]):
        if (smat[i,0] != curr_L):
            ret.append(oneSize(smat[startI:i,:],temp,betanu,z));
            startI = i;
            curr_L = smat[i,0];
    ret.apend(oneSize(smat[startI:,:],temp,betanu,z));
            

def findteq(mat,temp,betanu):
    betanu = given
    z = 0.0;
    dz = 0.1;
    for i in range(30):
        rescaled = analyze(mat,temp,betanu,z);
        for j in len(rescaled):
            #fit to exp func
            sp.optimize.curve_fit(lambda t,a,b,c: a*numpy.exp(b*t) + c,x,y,p0 = :wq


        z = z+ dz;


        }


