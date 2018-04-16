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
def calculate(mat,i,istart,FileList,function):
    #start by splitting by system size L
    submat = mat[istart:i,:];
    T = submat[0,1];
    llist,lind = np.unique(submat[:,0],return_index=True);
    N_L = llist.shape[0];
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
    for i in range(sortedMat.shape[0]):
        if (sortedMat[i,1] != T):
            calculate(sortedMat,i,ifirst,filelist,function);
            ifirst = i;
            T = sortedMat[i,1];
            
    #one final write
    calculate(sortedMat,i+1,ifirst,filelist,function);
