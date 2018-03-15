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


def openFiles(n,omega):
    odir = indexToString(n);
    directory = "./foutput/3DXY/rhos_omega/"+odir+"/"
    if not os.path.exists(directory):
        os.makedirs(directory);
    ofile1 = open("./foutput/3DXY/rhos_omega/"+odir+"/a4_8"+str(omega)+".dat","w");
    ofile2 = open("./foutput/3DXY/rhos_omega/"+odir+"/b8_16"+str(omega)+".dat","w");
    ofile3 = open("./foutput/3DXY/rhos_omega/"+odir+"/c16_32"+str(omega)+".dat","w");
    ofile4 = open("./foutput/3DXY/rhos_omega/"+odir+"/d32_64"+str(omega)+".dat","w");
    ofile5 = open("./foutput/3DXY/rhos_omega/"+odir+"/e64_128"+str(omega)+".dat","w");
    olist = [ofile1,ofile2,ofile3,ofile4,ofile5];
    return olist;

def getRS(e,sx,sy,sz,exp,L,T):
    rs = -L*e -(L*L*L*L/T)*(sx +sy +sz);
    rs = rs/(3.0*exp);
    return rs;

def getScalingCorrections(mat):
    e = mat[:,0];
    sx = mat[:,1];
    sy = mat[:,2];
    sz = mat[:,3];
    exp = mat[:,4];
    L = mat[:,5];
    T = mat[:,6];
    omega = mat[0,7];

    rs1 = getRS(e[0],sx[0],sy[0],sz[0],exp[0],L[0],T[0]);
    rs2 = getRS(e[1],sx[1],sy[1],sz[1],exp[1],L[1],T[1]);
    res = pow(L[0],omega)*(rs2-rs1);
    return [res];
def calcAvgs(mat):
    L = mat[0,0];
    T = mat[0,1];
    E = np.mean(mat[:,7]);
    S2X = np.mean(mat[:,14]);
    S2Y = np.mean(mat[:,15]);
    S2Z = np.mean(mat[:,16]);
    Exp = np.mean(mat[:,21]);
    omega = mat[0,22]
    return [E,S2X,S2Y,S2Z,Exp,L,T,omega]
    
def jackFunc(mat):
    llist,lind = np.unique(mat[:,0],return_index=True);
    if (llist.shape[0]<2):
        print(llist.shape);
        print("bad shape");
        exit();
    avgs = [];
    avgs.append(calcAvgs(mat[lind[0]:lind[1],:]));
    avgs.append(calcAvgs(mat[lind[1]:,:]));
    avgsmat = np.array(avgs);
    sc = getScalingCorrections(avgsmat);
    return sc;
    
#in goes all data for a specific temperature
def calculate(mat,i,ifirst,ofiles):
    submat = mat[ifirst:i,:];
    omega = submat[0,22];
    T = submat[0,1];
    llist,lind = np.unique(submat[:,0],return_index=True);
    N_L = llist.shape[0];
    N_corrs = N_L -1;
    lind = np.append(lind,-1);
    scalingcorr =[];
    delta = [];
    for x in range(N_corrs):
        submat2L = submat[lind[x]:lind[x+2],:];
        scalingcorr.append(jackFunc(submat2L));
        delta.append(jackknife.getJackDelta(submat2L,jackFunc,100));
    
    fstr= "{:30.30f}";
    ostr = "{:.5f}";
    for x in range(len(scalingcorr)):
        ofiles[x].write(fstr.format(T)+"    "+fstr.format(scalingcorr[x][0])+"    "+fstr.format(delta[x][0])+"    "+ostr.format(omega)+"\n")


# Format::
# 0      1      2      3      4      5      6            
# L      T      neqsw  neqcl  nsmsw  nsmcl  cold
#
# 7      8      9      10     11     12     13                
# E      E2     M      M2     M4     M2E    M4E
#
# 14     15     16     17     18     19     20     21                
# SX     SY     SZ     bin    dBdT   xi     rs     expFac
def getOmegaRange(ostart,oend,step):
    omegarange = [];
    omega = ostart;
    omegarange.append(ostart);
    while (omega < oend):
        omega = omega + step;
        omegarange.append(omega);
    return omegarange;

def selectK(L):
    if(L == 4):
        return 0
    if(L == 8):
        return 1
    if(L == 16):
        return 2
    if(L == 32):
        return 3
    if(L == 64):
        return 4
    if(L == 128):
        return 5
    
def analyze(mat,fName):
    #delete old data
    subprocess.call(['rm','-r','./foutput/3DXY/rhos_omega/']);
    subprocess.call(['mkdir','./foutput/3DXY/rhos_omega']);
    #sort indata
    ind = np.lexsort((mat[:,21],mat[:,20],mat[:,19],mat[:,18],mat[:,17],mat[:,16],mat[:,15],mat[:,14],mat[:,13],mat[:,12],mat[:,11],mat[:,10],mat[:,9],mat[:,8],mat[:,7],mat[:,5],mat[:,4],mat[:,3],mat[:,2],mat[:,6],mat[:,0],mat[:,1]));
    sortedMat = mat[ind];

    
    #define range of omegas
    TOL = 0.000001;
    orange = getOmegaRange(0.0,1.0,0.05);
    for n in range(len(orange)):
        omega = orange[n];
        omegavec = np.ones((sortedMat.shape[0],1));
        omegavec = omegavec*omega;
        omegamat = np.concatenate((sortedMat,omegavec),1);
        ifirst = 0;
        L = sortedMat[0,0];
        T = sortedMat[0,1];
        ofiles= openFiles(n,omega);
        for i in range(omegamat.shape[0]):
            if (omegamat[i,1] != T):
                calculate(omegamat,i,ifirst,ofiles);
                ifirst = i;
                T = omegamat[i,1];
        calculate(omegamat,-1,ifirst,ofiles);
