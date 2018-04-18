import os
import math
import subprocess
import numpy as np
import jackknife

def indexToString(n):
    digits = [];
    powers= [1000,100,10];
    i =0;
    frac =0;
    while True: 
        frac=int(n/powers[i]);
        i = i +1;
        digits.append(frac);
        if (frac != 0):
            digits.append(n%10);
            break;
        if (i == 3):
            digits.append(n%10);
            break;
    digits = [str(x) for x in digits];
    return ''.join(digits);


def openFiles(n,omega,dirname):
    odir = indexToString(n);
    directory = dirname + "/" + odir + "/"
    if not os.path.exists(directory):
        os.makedirs(directory);
    ofile1 = open(directory+"4_8_"+str(omega)+".dat","w");
    ofile2 = open(directory+"8_16_"+str(omega)+".dat","w");
    ofile3 = open(directory+"16_32_"+str(omega)+".dat","w");
    ofile4 = open(directory+"32_64_"+str(omega)+".dat","w");
    ofile5 = open(directory+"64_128_"+str(omega)+".dat","w");
    olist = [ofile1,ofile2,ofile3,ofile4,ofile5];
    return olist;

    
#in goes all data for a specific temperature
#first test how many L's are present
def calculate(mat,i,ifirst,function,ofiles):
    submat = mat[ifirst:i,:];
    omega = submat[0,-1];
    T = submat[0,1];
    llist,lind = np.unique(submat[:,0],return_index=True);
    N_L = llist.shape[0];
    N_corrs = N_L -1;
    if (N_L > 1 ):
        lind = np.append(lind,-1);
        scalingcorr =[];
        delta = [];
        for x in range(N_corrs):
            submat2L = submat[lind[x]:lind[x+2],:];
            scalingcorr.append(function(submat2L,omega));
            #delta.append(jackknife.getJackDelta(submat2L,lambda x: function(x,omega),100));
        
        fstr= "{:30.30f}";
        ostr = "{:.5f}";
        for x in range(len(scalingcorr)):
            #print(delta[x])
            ofiles[x].write(fstr.format(T)+"    "+fstr.format(scalingcorr[x])+"    "+fstr.format(0.00)+"    "+ostr.format(omega)+"\n")



    
def analyze(mat,dirname,function,orange):
    #delete old data
    subprocess.call(['rm','-r',dirname]);
    subprocess.call(['mkdir',dirname]);
    #sort indata by T first , then L.
    ind = np.lexsort((mat[:,0],mat[:,1]));
    sortedMat = mat[ind];
    
    #define range of omegas
    TOL = 0.00001;
    for n in range(len(orange)):
        omega = orange[n];
        ofiles= openFiles(n,omega,dirname);
        T_vals,T_inds =np.unique(sortedMat[:,1],return_index=True);
        T_inds = np.append(T_inds,-1);
        for i in range(len(T_vals)): 
                calculate(sortedMat,T_inds[i+1],T_inds[i],function,ofiles);
