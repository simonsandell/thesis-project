import numpy as np
import math

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
    S2X = np.mean(mat[:,14]);
    S2Y = np.mean(mat[:,15]);
    S2Z = np.mean(mat[:,16]);
    Exp = np.mean(mat[:,21]);
    return [E,S2X,S2Y,S2Z,Exp,L,T]

#values for 3 sizes goes in
def calcOmegaRS3L(mat):
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

