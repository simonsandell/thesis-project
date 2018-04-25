import pickle
import collections
import os
import sys

import pickler

fName = sys.argv[1];
load_failed = False;
indir = "./output/3DXY/";
datafile = open(indir+fName,"r");
data = [];
Avg = collections.namedtuple('Avg',['L','T',
    'Neqsw','Neqcl','NTotsw','NTotcl','cold',
    'e','e2','m','m2','m4','m2e','m4e','s2x','s2y','s2z',
    'bin','dbdt','chi','rs','expFac']);
for ln in datafile:
    strlist = ln.rsplit(" ");
    strlist = [x for x in strlist if not (x== "\n")];
    try:
        fllist = [float(x) for x in strlist];
        if (len(fllist) != 22):
            print('bad line at row ' + str(1 + len(data)));
        a = Avg(*fllist);
        data.append(a);
    except:
        print('bad data at row  ' + str(1 + len(data)));
        data.append(strlist);
        load_failed = True;
if (load_failed):
    exit(-1);
pickler.saveData(data,fName);
