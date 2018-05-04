import numpy as np
import conf
import collections

def calcIntersection(y1,y2,y3,y4,dT):
    px = dT*((y3-y1)/(y1 -y2 +y3 -y4));
    py = (y1*(y3 -y4) - y3*(y1-y2))/(y3 -y4 -y1 +y2);
    return [px,py];

def checkcheckIntersection(L1_T1,L2_T1,L1_T2,L2_T2):
    if ((L1_T1[1] -L2_T1[1])*(L1_T2[1] - L2_T2[1]) >0.0):
        return [False,0,0];
    else:
        [ix,iy] =calcIntersection(L1_T1[1],L1_T2[1],L2_T1[1],L2_T2[1],L1_T2[0] - L1_T1[0]);
        return [True,ix+L1_T1[0],iy];

def checkIntersection(LdictT1,LdictT2):
    res = [];
    for L in LdictT1.keys():
        for L2 in LdictT1.keys():
            if ((L*2) == L2):
                doesInt,ix,iy = checkcheckIntersection(
                        LdictT1[L],LdictT1[L2],LdictT2[L],LdictT2[L2]);
                if (doesInt):
                    res.append([ix,iy]);
    return res;

def getDist(xy,xy2):
    d = pow(pow(xy[0]-xy2[0],2) + pow(xy[1]-xy2[1],2),0.5);
    return d;

def calcANN(ints):
    nnd =[]
    for i in range(len(ints)):
        nnd.append(1000000.0);
        for j in range(len(ints)):
            if not (i==j):
                d = getDist(ints[i],ints[j]);
                if (d < nnd[i]):
                    nnd[i] = d;
    avgnnd = np.mean(nnd);
    return avgnnd;

quantStruct = collections.namedtuple('quantStruct',['Bin','Rs']);

def rescale(Tlist,omega):
    newTlist = [];
    for item in Tlist:
        newBinLdict = {};
        newRsLdict = {};
        for L,vallist in item.Bin.items():
            newBinList = vallist.copy();
            newBinList[1] = pow(newBinList[4],omega)*newBinList[1];
            newBinList[2] = pow(newBinList[4],omega)*newBinList[2];
            newBinLdict[L] = newBinList;
        for L,vallist in item.Rs.items():
            newRSList = vallist.copy();
            newRSList[1] = pow(newRSList[4],omega)*newRSList[1];
            newRSList[2] = pow(newRSList[4],omega)*newRSList[2];
            newRsLdict[L] = newRSList;
        newTlist.append(quantStruct(newBinLdict,newRsLdict));
    return newTlist;

def findBestIntersection(T_list,omegaList):
    intersections = [];
    Binres = [];
    Rsres = [];
    for omega in omegaList:
        T_list_resc = rescale(T_list,omega);
        intersections[:] = [];
        for struct1,struct2 in zip(T_list_resc[:-1],T_list_resc[1:]):
            intersections.extend(checkIntersection(struct1.Bin,struct2.Bin));
        print(len(intersections));
        avgNND = calcANN(intersections);
        Binres.append([omega,avgNND]);

    for omega in omegaList:
        T_list_resc = rescale(T_list,omega);
        intersections[:] = [];
        for struct1,struct2 in zip(T_list_resc[:-1],T_list_resc[1:]):
            intersections.extend(checkIntersection(struct1.Rs,struct2.Rs));
        avgNND = calcANN(intersections);
        Rsres.append([omega,avgNND,len(intersections)]);
    result = quantStruct(Binres,Rsres);
    return result;

