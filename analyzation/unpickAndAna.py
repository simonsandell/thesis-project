import conf
import pickle
import sys
import numpy as np
import collections
import pickler
import calculateAverages
import calculateScalingFuncs
import writeFoutput
import intersection
import scalingMethod

def getTdict(ldict):
    tdict = {};
    for L,td in ldict.items():
        for T,af in td.items():
            if T not in tdict:
                tdict[T] = {};
            tdict[T][L] = af;
    return tdict;
def getOmegaList():
    o = 0;
    oend = 2.0;
    dO = 0.05;
    ret = [];
    while (o< (oend+dO)):
        ret.append(o);
        o = o+dO;
    return ret;


fName = sys.argv[1];
conf.setModel(sys.argv[2]);
conf.setJackknifeBlock(int(sys.argv[3]))
conf.initNT();

L_dict = pickler.loadData(fName);
print("loading done");
T_dict = getTdict(L_dict);

#calculate easy averages
L_dict_avg = {};
L_dict_avg_alt = {};
for L,Tdict in L_dict.items():
    for T,avglist in Tdict.items():
        if not(L in L_dict_avg):
            L_dict_avg[L] ={};
            L_dict_avg_alt[L] = {};
        L_dict_avg[L][T] = calculateAverages.calcAvg(L_dict[L][T],L,T); 
        L_dict_avg_alt[L][T] = calculateAverages.calcAvgAlt(L_dict[L][T],L,T); 

writeFoutput.writeVsT(L_dict_avg,fName);
T_dict_avg = getTdict(L_dict_avg);
writeFoutput.writeVsL(T_dict_avg,fName);

writeFoutput.writeVsT(L_dict_avg_alt,fName+"_alt_");
T_dict_avg_alt = getTdict(L_dict_avg_alt);
writeFoutput.writeVsL(T_dict_avg_alt,fName+"_alt_");

#find intersection in binder and density
bInts = scalingMethod.binderIntersection(L_dict_avg);
rInts = scalingMethod.densityIntersection(L_dict_avg);
print(bInts);
writeFoutput.writeBinInt(bInts,fName);
writeFoutput.writeDenInt(rInts,fName);
#calculate tricky averages
T_omega_dict = {};
T_sc2quant_list=[];
for T,Ldict in sorted(T_dict.items()):
    T_omega_dict[T] = calculateScalingFuncs.calcSC3(Ldict,L_dict_avg,T);
    T_sc2quant_list.append(calculateScalingFuncs.calcSC2(Ldict,L_dict_avg,T));
writeFoutput.writeSC3(T_omega_dict,fName);
writeFoutput.writeSC2(T_sc2quant_list,fName);

##
#pickler.saveData(T_sc2quant_list,fName+"sc2quant");
#T_sc2quant_list = pickler.loadData(fName+"sc2quant");

# intersection
omegaList= getOmegaList();
sigmaVsOmega = intersection.findBestIntersection(T_sc2quant_list,omegaList);

writeFoutput.writeSigmaVsOmega(sigmaVsOmega,fName);

exit(0)
