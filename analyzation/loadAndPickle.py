import pickle
import collections
import os
import sys
import pickler
import conf

conf.initNT();

L_dict = {};
dirname = sys.argv[1];
for fName in os.listdir(dirname):
    if not (os.path.isdir(os.path.join(dirname,fName))):
        load_failed = False;
        datafile = open(os.path.join(dirname,fName),"r");
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
                    a = conf.MCAvg(*fllist);
                    if not a.L in L_dict:
                        L_dict[a.L] = {};
                    if not a.T in L_dict[a.L]:
                        L_dict[a.L][a.T] = [];
                    L_dict[a.L][a.T].append(a);
                except:
                    print(fName);
                    print(len(strlist));
                    print('bad line at row ' + str(1 + i));
                    load_failed = True;
if (load_failed):
    pickler.saveData(L_dict,fName+".somebadrows");
else:
    pickler.saveData(L_dict,fName);
