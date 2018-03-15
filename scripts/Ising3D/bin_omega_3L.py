import numpy as np
import math

def getBin(M2,M4,Exp):
    return M4*Exp/(M2*M2);

def getScalingCorrections(mat):
    m2 = mat[:,0];
    m4 = mat[:,1];
    exp = mat[:,2];

    b1 = getBin(m2[0],m4[0],exp[0]);
    b2 = getBin(m2[1],m4[1],exp[1]);
    b3 = getBin(m2[2],m4[2],exp[2]);
    div = (b3 -b2)/(b2-b1);
    if (div < 0):
        omega = 0.0;
    else:
        omega = -math.log(div)/math.log(2);
    return [omega];

def calcAvgs(mat):
    M2 = np.mean(mat[:,10]);
    M4 = np.mean(mat[:,11]);
    Exp = np.mean(mat[:,-1]);
    return [M2,M4,Exp]

#values for 3 system sizes goes in
def calcOmegaBin3L(mat):
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
