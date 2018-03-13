import numpy as np
import math
import jackknife

def openFiles():
    o1file = open("./foutput/3DXY/omega/omega1.dat","w")
    o2file = open("./foutput/3DXY/omega/omega2.dat","w")
    o3file = open("./foutput/3DXY/omega/omega3.dat","w")
    o4file = open("./foutput/3DXY/omega/omega4.dat","w")
    r1file = open("./foutput/3DXY/rs_corr/rscorr1.dat","w")
    r2file = open("./foutput/3DXY/rs_corr/rscorr2.dat","w")
    r3file = open("./foutput/3DXY/rs_corr/rscorr3.dat","w")
    r4file = open("./foutput/3DXY/rs_corr/rscorr4.dat","w")
    return [o1file,o2file,o3file,o4file,r1file,r2file,r3file,r4file];

def getBin(M2,M4,Exp):
    return M4*Exp/(M2*M2);

def getRS(e,sx,sy,sz,exp,L,T):
    rs = -L*e -(L*L*L*L/T)*(sx +sy +sz);
    rs = rs/(3.0*exp);
    return rs;

def getScalingCorrections(mat):
    e = mat[:,0];
    m2 = mat[:,1];
    m4 = mat[:,2];
    sx = mat[:,3];
    sy = mat[:,4];
    sz = mat[:,5];
    exp = mat[:,6];
    L = mat[:,7];
    T = mat[:,8];

    b1 = getBin(m2[0],m4[0],exp[0]);
    b2 = getBin(m2[1],m4[1],exp[1]);
    b3 = getBin(m2[2],m4[2],exp[2]);
    div = (b3 -b2)/(b2-b1);
    omega = -math.log(div)/math.log(2);
    rs1 = getRS(e[0],sx[0],sy[0],sz[0],exp[0],L[0],T[0]);
    rs2 = getRS(e[1],sx[1],sy[1],sz[1],exp[1],L[1],T[1]);
    rs3 = getRS(e[2],sx[2],sy[2],sz[2],exp[2],L[2],T[2]);
    rdiv = (rs3-rs2)/(rs2-rs1);
    if (rdiv > 0):
        romega = -math.log(rdiv)/math.log(2);
    else:
        romega = 0;
    return [omega,romega];

def calcAvgs(mat):
    L = mat[0,0];
    T = mat[0,1];
    E = np.mean(mat[:,7]);
    M2 = np.mean(mat[:,10]);
    M4 = np.mean(mat[:,11]);
    S2X = np.mean(mat[:,14]);
    S2Y = np.mean(mat[:,15]);
    S2Z = np.mean(mat[:,16]);
    Exp = np.mean(mat[:,21]);
    return [E,M2,M4,S2X,S2Y,S2Z,Exp,L,T]

#values for 3 sizes goes in
def jackFunc(mat):
    llist,lind = np.unique(mat[:,0],return_index=True);
    if (llist.shape[0] < 3):
        print(llist.shape)
        print("bad shape");
        exit()
    avgs = [];
    avgs.append(calcAvgs(mat[lind[0]:lind[1],:]));
    avgs.append(calcAvgs(mat[lind[1]:lind[2],:]));
    avgs.append(calcAvgs(mat[lind[2]:,:]));
    avgsmat = np.array(avgs);
    scs = getScalingCorrections(avgsmat);
    return scs;
    

#in goes all data for a specific temperature
def calculate(mat,i,istart,FileList):
# Format::
# 0      1      2      3      4      5      6            
# L      T      neqsw  neqcl  nsmsw  nsmcl  cold
#
# 7      8      9      10     11     12     13                
# E      E2     M      M2     M4     M2E    M4E
#
# 14     15     16     17     18     19     20     21                
# S2X    S2Y    S2Z    bin    dBdT   xi     rs     expFac
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
        scalingcorrs.append(jackFunc(submat3L));
        deltas.append(jackknife.getJackDelta(submat3L,jackFunc,100));

    fstr= "{:30.30f}";
    for x in range(len(scalingcorrs)):

        FileList[x].write(fstr.format(T) + "    " + fstr.format(scalingcorrs[x][0]) + "    " + fstr.format(deltas[x][0]) + " \n"); 

        FileList[x+4].write(fstr.format(T) + "    " + fstr.format(scalingcorrs[x][1]) + "    " + fstr.format(deltas[x][1]) + " \n"); 



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
def analyze(mat,fName):
    #Sort input data, by temperature, then L
    ind = np.lexsort((mat[:,21],mat[:,20],mat[:,19],mat[:,18],mat[:,17],mat[:,16],mat[:,15],mat[:,14],mat[:,13],mat[:,12],mat[:,11],mat[:,10],mat[:,9],mat[:,8],mat[:,7],mat[:,5],mat[:,4],mat[:,3],mat[:,2],mat[:,6],mat[:,0],mat[:,1]));
    sortedMat = mat[ind];
    #form averages and print to file
    T = sortedMat[0,1];
    
    TOL = 0.000001;
    ifirst = 0;
    filelist = openFiles();
    for i in range(sortedMat.shape[0]):
        if (sortedMat[i,1] != T):
            calculate(sortedMat,i,ifirst,filelist);
            ifirst = i;
            T = sortedMat[i,1];
            
    #one final write
    calculate(sortedMat,i+1,ifirst,filelist);
