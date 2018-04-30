import pickle
import collections
import os
import sys
import pickler

fName = sys.argv[1];
load_failed = False;
indir = "./output/3DXY/";
datafile = open(indir+fName,"r");
MCAvg = collections.namedtuple('MCAvg',[
    'Neqsw','Neqcl','NTotsw','NTotcl','cold',
    'e','e2','m','m2','m4','m2e','m4e','s2x','s2y','s2z',
    'bin','dbdt','chi','rs','expFac']);
T_dict_4 = {};
T_dict_8 = {};
T_dict_16 = {};
T_dict_32 = {};
T_dict_64 = {};
T_dict_128 = {};
L_dict = {4:T_dict_4,
          8:T_dict_8,
          16:T_dict_16,
          32:T_dict_32,
          64:T_dict_64,
          128:T_dict_128
          };
i = 0;
for ln in datafile:
    i = i+1;
    strlist = ln.rsplit(" ");
    strlist = [x for x in strlist if not (x== "\n")];
    if not (strlist[0] == "#"):
        try:
            fllist = [float(x) for x in strlist];
            if (len(fllist) != 22):
                print('bad line at row ' + str(1 + i));
            a = MCAvg(*(fllist[2:]));
            ln_L = int(fllist[0] +0.1);
            if fllist[1] in L_dict[ln_L]:
                L_dict[ln_L][fllist[1]].append(a);
            else:
                L_dict[ln_L][fllist[1]] = [a];
        except:
            print('bad line at row ' + str(1 + i));
            load_failed = True;
if (load_failed):
    pickler.saveData(L_dict,fName+"somebadrows");
else:
    pickler.saveData(L_dict,fName);
