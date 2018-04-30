import conf
import pickle
import sys
import numpy as np
import collections
import pickler
import calculateAverages
import calculateScalingFuncs
import writeFoutput

def getTdict(ldict):
    tdict = {};
    for L,td in ldict.items():
        for T,af in td.items():
            if T not in tdict:
                tdict[T] = {};
            tdict[T][L] = af;
    return tdict;

fName = sys.argv[1];
conf.setModel(sys.argv[2]);
if (conf.model == "3DXY"):
    avgF = collections.namedtuple('avgF',['E','M','Bin','dBdT','Chi','Rs','dE',  'dM','dBin','ddBdT','dChi','dRs']);
    MCAvg = collections.namedtuple('MCAvg',['L','T',
    'Neqsw','Neqcl','NTotsw','NTotcl','cold',
    'e','e2','m','m2','m4','m2e','m4e','s2x','s2y','s2z',
    'bin','dbdt','chi','rs','expFac']);

L_dict = pickler.loadData(fName);
print("loading done");
T_dict = getTdict(L_dict);

#calculate easy averages
L_dict_avg = {};
for L,Tdict in L_dict.items():
    for T,avglist in Tdict.items():
        if not(L in L_dict_avg):
            L_dict_avg[L] ={};
        L_dict_avg[L][T] = calculateAverages.calcAvg(L_dict[L][T],L,T); 

#calculate tricky averages
T_omega_dict = {};
T_sc2quant_list=[];
for T,Ldict in sorted(T_dict.items()):
    T_omega_dict[T] = calculateScalingFuncs.calcSC3(Ldict,L_dict_avg);
    T_sc2quant_list.append(calculateScalingFuncs.calcSC2(Ldict,L_dict_avg));

# intersection
sigmavsomega = intersection.findBestIntersection(T_sc2quant_list);




writeFoutput.writeSC3(T_omega_dict,fName);
writeFoutput.writeSC2(T_sc2quant_list,fName);


writeFoutput.writeVsT(L_dict_avg,fName);
writeFoutput.writeVsL(L_dict_avg,fName);
