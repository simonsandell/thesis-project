import numpy as np

def getBin(M2,M4,Exp):
    return M4*Exp/(M2*M2);

def getScalingCorrections(mat):
    m2 = mat[:,0];
    m4 = mat[:,1];
    exp = mat[:,2];
    omega = mat[0,3];
    L = mat[:,4];

    b1 = getBin(m2[0],m4[0],exp[0]);
    b2 = getBin(m2[1],m4[1],exp[1]);

    res = pow(L[0],omega)*(b2-b1);
    return [res];

def calcAvgs(mat):
    M2 = np.mean(mat[:,10]);
    M4 = np.mean(mat[:,11]);
    Exp = np.mean(mat[:,-2]);
    omega = mat[0,-1]
    L = mat[0,0]
    return [M2,M4,Exp,omega,L]
#takes matrix with 2 sizes of L    
def calcOmegaBin2L(mat):
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
