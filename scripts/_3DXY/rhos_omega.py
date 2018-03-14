import os
import subprocess
import numpy as np
import jackknife

def indexToString(n):
    return chr(n + ord('a'));



def openFile(n,omega):
    odir = indexToString(n);
    directory = "./foutput/3DXY/rhos_omega/"+odir+"/"
    if not os.path.exists(directory):
        os.makedirs(directory);
    ofile1 = open("./foutput/3DXY/rhos_omega/"+odir+"/a4"+str(omega)+".dat","w");
    ofile2 = open("./foutput/3DXY/rhos_omega/"+odir+"/b8"+str(omega)+".dat","w");
    ofile3 = open("./foutput/3DXY/rhos_omega/"+odir+"/c16"+str(omega)+".dat","w");
    ofile4 = open("./foutput/3DXY/rhos_omega/"+odir+"/d32"+str(omega)+".dat","w");
    ofile5 = open("./foutput/3DXY/rhos_omega/"+odir+"/e64"+str(omega)+".dat","w");
    ofile6 = open("./foutput/3DXY/rhos_omega/"+odir+"/f128"+str(omega)+".dat","w");
    olist = [ofile1,ofile2,ofile3,ofile4,ofile5,ofile6];
    return olist;

def getRSomega(e,sx,sy,sz,exp,L,T,omega):
    rs = -L*e -(L*L*L*L/T)*(sx +sy +sz);
    rs = rs/(3.0*exp);
    rs = rs*pow(L,-omega);
    return rs;

def jackFunc(mat):
    rso = getRSomega(np.mean(mat[:,7]),np.mean(mat[:,14]),np.mean(mat[:,15]),np.mean(mat[:,16]),np.mean(mat[:,21]),np.mean(mat[0,0]),np.mean(mat[0,1]),np.mean(mat[0,22]));
    return np.matrix(rso);
    
def calculate(mat,i,ifirst,ofile):
    submat = mat[ifirst:i,:];
    omega = submat[0,22];
    N = i-ifirst;
    T = submat[0,1];
    fstr= "{:30.30f}";
    betweenstring = "&\n@redraw\n@sleep 0.5\n@with g0\n@kill s0\n@s0 type xydy\n"
    betweensetstring = "&\n@with g0\n@kill s1\n@s1 type xydy\n"
    function = jackFunc(submat);
    delta = jackknife.getJackDelta(submat,jackFunc,10);
    ofile.write(fstr.format(T)+"    "+fstr.format(function.flat[0])+"    "+fstr.format(delta[0])+"    "+repr(omega)+"\n")


# Format::
# 0      1      2      3      4      5      6            
# L      T      neqsw  neqcl  nsmsw  nsmcl  cold
#
# 7      8      9      10     11     12     13                
# E      E2     M      M2     M4     M2E    M4E
#
# 14     15     16     17     18     19     20     21                
# SX     SY     SZ     bin    dBdT   xi     rs     expFac
def getOmegaRange(ostart,oend,N):
    omegarange = [];
    for x in range(N):
        omegarange.append(ostart + (x/(N-1.0))*(oend-ostart));
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
def rmOldData():
    subprocess.call(['rm','-r','./foutput/3DXY/rhos_omega/']);
    subprocess.call(['mkdir','./foutput/3DXY/rhos_omega']);
    

def analyze(mat,fName):
    rmOldData();
    ind = np.lexsort((mat[:,21],mat[:,20],mat[:,19],mat[:,18],mat[:,17],mat[:,16],mat[:,15],mat[:,14],mat[:,13],mat[:,12],mat[:,11],mat[:,10],mat[:,9],mat[:,8],mat[:,7],mat[:,5],mat[:,4],mat[:,3],mat[:,2],mat[:,6],mat[:,1],mat[:,0]));
    sortedMat = mat[ind];
    #form averages and print to file
    
    TOL = 0.000001;
    orange = getOmegaRange(0.0,0.05,21);
    for n in range(len(orange)):
        omega = orange[n];
        omegavec = np.ones((sortedMat.shape[0],1));
        omegavec = omegavec*omega;
        omegamat = np.concatenate((sortedMat,omegavec),1);
        k = 0;
        ifirst = 0;
        L = sortedMat[0,0];
        T = sortedMat[0,1];
        ofile = openFile(n,omega);
        for i in range(omegamat.shape[0]):
            if (omegamat[i,1] != T):
                calculate(omegamat,i,ifirst,ofile[k]);
                ifirst = i;
                T = omegamat[i,1];
            if (omegamat[i,0] != L):
                L = omegamat[i,0];
                k = selectK(L);
        calculate(omegamat,-1,ifirst,ofile[k]);
