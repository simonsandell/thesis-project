import numpy as np
import collections
import math
import jackknife

def splitL(Llist,Lval):
    L1list =[];
    L2list=[];
    L4list=[];
    for item in Llist:
        if item.L == Lval[0]:
            L1list.append(item);
        if item.L == Lval[1]:
            L2list.append(item);
        if item.L == Lval[2]:
            L4list.append(item);
    return [L1list,L2list,L4list];

def calcOmega(q,q2,q4):
    omega = -(1.0/np.log(2))*(np.log(q4-q2) - np.log(q2-q));
    return omega;

def calcB(llist):
    n = len(llist);
    avgm2 = 0.0;
    avgm4 = 0.0;
    avgEF = 0.0;
    for item in llist:
        avgm2 += item.m2;
        avgm4 += item.m4;
        avgEF += item.expFac;
    avgm2 /= n;
    avgm4 /= n;
    avgEF /= n;
    return (avgm4*avgEF/pow(avgm2,2));

def calcRS(llist):
    n = len(llist);
    L = llist[0].L;
    T = llist[0].T;
    avgE = 0.0;
    avgs2x = 0.0;
    avgs2y = 0.0;
    avgs2z = 0.0;
    avgEF = 0.0;
    for item in llist:
        avgE += item.E;
        avgs2x += item.s2x;
        avgs2y += item.s2y;
        avgs2z += item.s2z;
        avgEF += item.expFac;
    avgE /= n;
    avgs2x /= n;
    avgs2y /= n;
    avgs2z /= n;
    avgEF /= n;
    RS = -L*avgE - (pow(L,4)/T)*(avgs2x + avgs2y + avgs2z);
    RS = RS/(3.0*avgEF);
    return RS;

def jf_SC3(Lcombined,Lval):
    [ll,ll2,ll4] = splitL(Lcombined,Lval);
    b = calcB(ll);
    b2 = calcB(ll2);
    b4 = calcB(ll4);
    retB = calcOmega(b,b2,b4);

    r = calcB(ll);
    r2 = calcB(ll2);
    r4 = calcB(ll4);
    retR = calcOmega(r,r2,r4);
    return [retB,retR];

def calcSC3(ldict,ldict_avg,temp):
    omegaBinderRes = {};
    omegaRsRes = {};
    Llist = sorted(list(ldict.keys()));
    if (len(Llist)>2):
        Llist1 = Llist[:-2];
        Llist2 = Llist[1:-1];
        Llist3 = Llist[2:];
        for L1,L2,L3 in zip(Llist1,Llist2,Llist3):
            if ((not L1*2 == L2) or (not L2*2==L3)):
                print('calcSC3: L not powers of 2');
            omegaB = calcOmega(ldict_avg[L1][temp].Bin,ldict_avg[L2][temp].Bin,ldict_avg[L3][temp].Bin);
            omegaRS = calcOmega(ldict_avg[L1][temp].Rs,ldict_avg[L2][temp].Rs,ldict_avg[L3][temp].Rs);
            # delta omega
            # combine into single list
            Lcombined = ldict[L1] + ldict[L2] + ldict[L3];
            N = len(Lcombined);
            deltaOmega = jackknife.getJackDelta(Lcombined,lambda x: jf_SC3(x,[L1,L2,L3]),100);
            if not L1 in omegaBinderRes:
                omegaBinderRes[L1] = [];
            omegaBinderRes[L1].append([temp,omegaB,deltaOmega[0],L1,L2,L3,N]);
            if not L1 in omegaRsRes:
                omegaRsRes[L1] = [];
            omegaRsRes[L1].append([temp,omegaRS,deltaOmega[1],L1,L2,L3,N]);
    omegaStruct = collections.namedtuple('omegaStruct',['Bin','Rs']); 
    ret = omegaStruct(omegaBinderRes,omegaRsRes);
    return ret;

def calcSC2Quant(q,q2,omega,L):
    ret =  pow(L,omega)*(q2 - q);
    return ret;

def jf_SC2(Lcomb,omega,L):
    [Llist,L2list,] = splitL(Lcomb,L);
    b = calcB(Llist);
    b2 = calcB(L2list);
    r = calcRS(Llist);
    r2 = calcRS(L2list);
    bQuant = calcSC2Quant(b,b2,omega,L[0]);
    rQuant = calcSC2Quant(r,r2,omega,L[0]);

    return [bQuant,rQuant];


def calcSC2(ldict,ldict_avg,temp):
        omDictRS = {}
        omDictBin = {}
        O = 0;
        dO = 0.05;
        orange = [];
        while (O < (1.5+dO)):
            orange.append(O);
            omDictRS[O] = {};
            omDictBin[O] = {};
            O = O+dO;
        Llist = sorted(list(ldict.keys()));
        Llist1 = Llist[:len(Llist)-1];
        Llist2 = Llist[1:];
        for L1,L2 in zip(Llist1,Llist2):
            for omega in orange:
                quantBin = calcSC2Quant(ldict_avg[L1][temp].Bin,ldict_avg[L2][temp].Bin,
                        omega,L1);
                quantRs = calcSC2Quant(ldict_avg[L1][temp].Rs,ldict_avg[L2][temp].Rs,
                        omega,L1);

                # combine lists for jackknifing
                Lcomb = ldict[L1] + ldict[L2];
                N = len(Lcomb);
                deltaQuant = jackknife.getJackDelta(Lcomb,
                        lambda x: jf_SC2(x,omega,[L1,L2,0]), 100);

                if not L1 in omDictBin[omega]:
                    omDictBin[omega][L1] = [];
                omDictBin[omega][L1].append([temp,quantBin,deltaQuant[0],omega,L1,L2,N]);
                if not L1 in omDictRs[omega]:
                    omDictRs[omega][L1] = [];
                omDictRs[omega][L1].append([temp,quantRs,deltaQuant[1],omega,L1,L2,N]);
    sc2QuantStruct = collections.namedtuple('sc2QuantStruct',['Bin','Rs']);
    return sc2QuantStruct(omDictBin,omDictRs);

