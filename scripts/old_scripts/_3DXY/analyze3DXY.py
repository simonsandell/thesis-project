import numpy as np
import math
import jackknife
np.set_printoptions(threshold=np.nan)

def getBin(m2,m4,exp):
    return (m4*exp)/(m2*m2);

def getdBdT(M2,M4,M2E,M4E,E,Exp,T,Nspins):
    dbdt= Exp*M4E*M2 + M4*M2*E - 2.0*M4*M2E*Exp;
    dbdt= Nspins*dbdt/(T*T*M2*M2*M2);
    return dbdt;
def getXI(m,m2,exp,T,Nspins):
    return Nspins*(m2/exp - m*m/(exp*exp))/T
def getRS(e,sx,sy,sz,exp,L,T):
    rs = -L*e -(L*L*L*L/T)*(sx +sy +sz);
    rs = rs/(3.0*exp);
    return rs;

def calc_vsT(mat):
    avgs = [];
    L = mat[0,0];
    T = mat[0,1];
    Nspins = L*L*L;
    interestingMeans = [7,9,10,11,12,13,14,15,16,21];
    for x in interestingMeans:
        avgs.append(np.mean(mat[:,x]));
    res = [];    
    res.append(avgs[0]/avgs[9]);
    res.append(avgs[1]/avgs[9]);
    res.append(getBin(avgs[2],avgs[3],avgs[9]));
    res.append(getdBdT(avgs[2],avgs[3],avgs[4],avgs[5],avgs[0],avgs[9],T,Nspins));
    res.append(getXI(avgs[1],avgs[2],avgs[9],T,Nspins));
    res.append(getRS(avgs[0],avgs[6],avgs[7],avgs[8],avgs[9],L,T));
    return res;
# Format::
# 0      1      2      3      4      5      6            
# L      T      neqsw  neqcl  nsmsw  nsmcl  cold
#
# 7      8      9      10     11     12     13                
# E      E2     M      M2     M4     M2E    M4E
#
# 14     15     16     17     18     19     20     21                
# SX     SY     SZ     bin    dBdT   xi     rs     expFac
