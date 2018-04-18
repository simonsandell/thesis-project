import numpy as np
import subprocess
import math
import jackknife

def openFiles(directory):
    o1file = open(directory+"/omega1.dat","w")
    o2file = open(directory+"/omega2.dat","w")
    o3file = open(directory+"/omega3.dat","w")
    o4file = open(directory+"/omega4.dat","w")
    return [o1file,o2file,o3file,o4file];

    

#in goes all data for a specific temperature
def calculate(mat,i,istart,FileList,function,linds):
    T = mat[istart,1];
    N_L = linds.shape[0];
    N_corrs = N_L -2;
    lind = np.append(lind,-1);
    scalingcorrs = [];
    deltas = [];
    for x in range(N_corrs):
        submat3L = submat[lind[x]:lind[x+3],:];
        scalingcorrs.append(function(submat3L));
        deltas.append(jackknife.getJackDelta(submat3L,function,100));

    fstr= "{:30.30f}";
    for x in range(len(scalingcorrs)):

        FileList[x].write(fstr.format(T) + "    " + fstr.format(scalingcorrs[x][0]) + "    " + fstr.format(deltas[x][0]) + " \n"); 




#
#read raw data from file in ./output
##########################################################
# Format::
# 0      1      2      3      4      5      6            
# L      T      neqsw  neqcl  nsmsw  nsmcl  cold
#
# 7      8      9      10     11     12     13                
# E      E2     M      M2     M4     M2E    M4E
#
# 14     15     16     17     18     19     20     21                
# SX     SY     SZ     bin    dBdT   xi     rs     expFac
def analyze(mat,dirname,function):
    #Sort input data, by temperature, then L
    ind = np.lexsort((mat[:,0],mat[:,1]));
    sortedMat = mat[ind];
    #form averages and print to file
    T = sortedMat[0,1];
    TOL = 0.000001;
    ifirst = 0;
    filelist = openFiles(dirname);
    T_vals,T_inds =np.unique(sortedMat[:,1],return_index=True);
    T_inds = np.append(T_inds,-1);
    for i in range(len(T_vals)):
        L_vals,L_inds = np.unique(sortedMat[T_inds[i]:T_inds[i+1],0],return_index=True);
        if (len(L_vals) > 2):
            calculate(sortedMat,T_inds[i+1],T_inds[i],filelist,function,L_inds);
