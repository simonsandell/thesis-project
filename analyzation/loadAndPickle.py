import pickle
import collections
import os
import sys
import pickler

fName = sys.argv[1];
load_failed = False;
indir = "./output/3DXY/";
datafile = open(indir+fName,"r");
MCAvg = collections.namedtuple('MCAvg',['L','T',
    'Neqsw','Neqcl','NTotsw','NTotcl','cold',
    'e','e2','m','m2','m4','m2e','m4e','s2x','s2y','s2z',
    'bin','dbdt','chi','rs','expFac']);

L_dict = {};
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

            a = MCAvg(*fllist);
            if not a.T in L_dict[a.L]:
                L_dict[a.L][a.T] = [];
            L_dict[a.L][a.T].append(a);
        except:
            print('bad line at row ' + str(1 + i));
            load_failed = True;
if (load_failed):
    pickler.saveData(L_dict,fName+".somebadrows");
else:
    pickler.saveData(L_dict,fName);
