import numpy as np
import jackknife
import collections
import conf

avgF = collections.namedtuple('avgF',['E','M','Bin','dBdT','Chi','Rs','dE',  'dM','dBin','ddBdT','dChi','dRs']);

def jf3DXY(avglist,L,T):
    N = len(avglist);
    Nspins = pow(L,3);
    avg_e =0;
    avg_e2 =0;
    avg_m =0;
    avg_m2 =0;
    avg_m4 =0;
    avg_m2e =0;
    avg_m4e =0;
    avg_s2x =0;
    avg_s2y =0;
    avg_s2z =0;
    avg_expFac =0;
    for mcavg in avglist:
        avg_e += mcavg.e;
        avg_e2 += mcavg.e2;
        avg_m += mcavg.m;
        avg_m2 += mcavg.m2;
        avg_m4 += mcavg.m4;
        avg_m2e += mcavg.m2e;
        avg_m4e += mcavg.m4e;
        avg_s2x += mcavg.s2x;
        avg_s2y += mcavg.s2y;
        avg_s2z += mcavg.s2z;
        avg_expFac += mcavg.expFac;
    avg_e /= N   
    avg_e2 /= N 
    avg_m /= N 
    avg_m2 /= N 
    avg_m4 /= N 
    avg_m2e /= N
    avg_m4e /= N
    avg_s2x /= N
    avg_s2y /= N
    avg_s2z /= N
    avg_expFac /= N
    E = avg_e /avg_expFac;
    M = avg_m /avg_expFac;
    Bin = avg_m4*avg_expFac /(avg_m2*avg_m2);
    dBdT = avg_expFac*avg_m4e*avg_m2 + avg_m4*avg_m2*avg_e - 2.0*avg_m4*avg_m2e*avg_expFac;
    dBdT= Nspins*dBdT/(pow(T,2)*pow(avg_m2,3));
    Chi = (Nspins/T)*(avg_m2/avg_expFac - pow(avg_m,2)/(pow(avg_expFac,2)));
    Rs = -L*avg_e - (pow(L,4)/T)*(avg_s2x + avg_s2y + avg_s2z);
    Rs = Rs/(3.0*avg_expFac);
    return [E,M,Bin,dBdT,Chi,Rs];

def calcAvg(MCAvgList,L,T):
    if (conf.model == "3DXY"):
        jackfunc = jf3DXY;
    func_avg = jackfunc(MCAvgList,L,T);
    if (conf.jackknife_on):
        delta_func = jackknife.getJackDelta(MCAvgList,lambda x: jackfunc(x,L,T),conf.jackknife_blocks);
    else:
        delta_func = [0,0,0,0,0,0];
    f = func_avg;
    f.extend(delta_func);
    result = avgF(*f);
    return result;
    


     
