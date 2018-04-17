import numpy as np

def calcSC2BinQuant(mat,omega,lind):
    l0 = lind[0];
    l1 = lind[1];
    B_0 = np.mean(mat[l0:l1,11])*np.mean(mat[l0:l1,-2])/pow(np.mean(mat[l0:l1,10]),2);
    B_1 = np.mean(mat[l1:,11])*np.mean(mat[l1:,-2])/pow(np.mean(mat[l1:,10]),2);
    quant = pow(mat[l0,0],omega)*(B_1 - B_0)
    return quant;

#takes matrix with 2 sizes of L, calculates the quantity L^w * (2L*rs(2L) - L*rs(L))
def SC2LBin(mat,omega):
    llist,lind = np.unique(mat[:,0],return_index=True);
    if (llist.shape[0]<2):
        print(llist.shape);
        print("bad shape");
        return -1;
    else:
        return calcSC2BinQuant(mat,omega,lind);
