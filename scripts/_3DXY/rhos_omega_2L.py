import numpy as np

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
    
def calcOmegaRS2L(mat):
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
