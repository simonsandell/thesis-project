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
    ofile1 = open(directory+"04_8"+str(omega)+".dat","w");
    ofile2 = open(directory+"08_16"+str(omega)+".dat","w");
    ofile3 = open(directory+"16_32"+str(omega)+".dat","w");
    ofile4 = open(directory+"32_64"+str(omega)+".dat","w");
    ofile5 = open(directory+"64_128"+str(omega)+".dat","w");
    olist = [ofile1,ofile2,ofile3,ofile4,ofile5];
    return olist;

    
#in goes all data for a specific temperature
def calculate(mat,i,ifirst,ofiles,function):
    submat = mat[ifirst:i,:];
    omega = submat[0,-1];
    T = submat[0,1];
    llist,lind = np.unique(submat[:,0],return_index=True);
    N_L = llist.shape[0];
    N_corrs = N_L -1;
    if (N_corrs == 0):
        print(llist);
        print("too few L's")
        exit();
    lind = np.append(lind,-1);
    scalingcorr =[];
    delta = [];
    for x in range(N_corrs):
        submat2L = submat[lind[x]:lind[x+2],:];
        scalingcorr.append(function(submat2L));
        delta.append(jackknife.getJackDelta(submat2L,function,100));
    
    fstr= "{:30.30f}";
    ostr = "{:.5f}";
    for x in range(len(scalingcorr)):
        ofiles[x].write(fstr.format(T)+"    "+fstr.format(scalingcorr[x][0])+"    "+fstr.format(delta[x][0])+"    "+ostr.format(omega)+"\n")



    
def analyze(mat,dirname,function,orange):
    #delete old data
    subprocess.call(['rm','-r',dirname]);
    subprocess.call(['mkdir',dirname]);
    #sort indata
    ind = np.lexsort((mat[:,0],mat[:,1]));
    sortedMat = mat[ind];
    
    #define range of omegas
    TOL = 0.000001;
    for n in range(len(orange)):
        omega = orange[n];
        omegavec = np.ones((sortedMat.shape[0],1));
        omegavec = omegavec*omega;
        omegamat = np.concatenate((sortedMat,omegavec),1);
        ifirst = 0;
        L = sortedMat[0,0];
        T = sortedMat[0,1];
        ofiles= openFiles(n,omega,dirname);
        for i in range(omegamat.shape[0]):
            if (omegamat[i,1] != T):
                calculate(omegamat,i,ifirst,ofiles,function);
                ifirst = i;
                T = omegamat[i,1];
        calculate(omegamat,-1,ifirst,ofiles,function);
