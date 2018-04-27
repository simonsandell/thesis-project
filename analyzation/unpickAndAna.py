import pickle
import sys
import numpy as np
import collections
import pickler
import calculateAverages
import calculateScalingFuncs
import writeFoutput


fName = sys.argv[1];
model = sys.argv[2];
if (model == "3DXY"):
    avgF = collections.namedtuple('avgF',['E','M','Bin','dBdT','Chi','Rs','dE',  'dM','dBin','ddBdT','dChi','dRs']);
    MCAvg = collections.namedtuple('MCAvg',[
    'Neqsw','Neqcl','NTotsw','NTotcl','cold',
    'e','e2','m','m2','m4','m2e','m4e','s2x','s2y','s2z',
    'bin','dbdt','chi','rs','expFac']);

L_dict = pickler.loadData(fName);
print("load done");

T_avg_4 = {};
T_avg_8 = {};
T_avg_16 = {};
T_avg_32 = {};
T_avg_64 = {};
T_avg_128 = {};
L_dict_avg = {4:T_avg_4,
          8:T_avg_8,
          16:T_avg_16,
          32:T_avg_32,
          64:T_avg_64,
          128:T_avg_128
          };
for L,Tdict in L_dict.items():
    for T,avglist in Tdict.items():
       L_dict_avg[L][T] = calculateAverages.calcAvg(L_dict[L][T],L,T,model); 

T_dict_avg = writeFoutput.getTdict(L_dict_avg);
omegaDictsSC2 = calculateScalingFuncs.calcSC2(T_dict_avg,model);
omegaDictsSC3 = calculateScalingFuncs.calcSC3(T_dict_avg,model);

writeFoutput.writeSC2(omegaDictsSC2,fName,model);
writeFoutput.writeSC3(omegaDictsSC3,fName,model);
writeFoutput.writeVsT(L_dict_avg,fName,model);
writeFoutput.writeVsL(L_dict_avg,fName,model);

    
