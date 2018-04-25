import numpy as np

def calcSC2RhoQuant(mat,omega,lind):
    l0 = lind[0];
    l1 = lind[1];
    L0 = mat[l0,0];
    L1 = mat[l1,0];
    T0 = mat[l0,1];
    T1 = mat[l1,1];
    rho_0 = -L0*np.mean(mat[l0:l1,7]) -  (pow(L0,4)/T0)*(np.mean(mat[l0:l1,14]) +
        np.mean(mat[l0:l1,15]) + np.mean(mat[l0:l1,16]));
    rho_0 = rho_0/(3*np.mean(mat[l0:l1,-1]));
    rho_1 = -L1*np.mean(mat[l1:,7]) -  (pow(L1,4)/T1)*(np.mean(mat[l1:,14]) +
        np.mean(mat[l1:,15]) + np.mean(mat[l1:,16]));
    rho_1 = rho_1/(3*np.mean(mat[l1:,-1]));
        
    quant = pow(mat[l0,0],omega)*(rho_1 - rho_0)
    return quant;

#takes matrix with 2 sizes of L, calculates the quantity L^w * (2L*rs(2L) - L*rs(L))
def SC2LRho(mat,omega):
    llist,lind = np.unique(mat[:,0],return_index=True);
    if (llist.shape[0]<2):
        print(llist.shape);
        print("bad shape");
        return -1;
    else:
        return calcSC2RhoQuant(mat,omega,lind);

