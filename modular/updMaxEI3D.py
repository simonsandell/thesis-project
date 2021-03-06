import subprocess
import os

list4 = [];
list8 = [];
list16 = [];
list32 = [];
list64 = [];
list128 = [];

lists = { 4:list4,
        8:list8,
        16:list16,
        32:list32,
        64:list64,
        128:list128
        }

directory = "/home/simon/exjobb/modular/maxE/Ising3D/";
for filename in os.listdir(directory):
    strL = filename.rsplit("_")
    L = int(strL[0]);
    fpath = directory + filename;
    Rfile = open(directory+filename,"r")
    val = float(Rfile.read())
    lists[L].append(val);

for l in lists:
    maxV = 0;
    for v in lists[l]:
        if (abs(v) > abs(maxV)):
            maxV = v;
    Wfile = open(directory + str(l) + "_maxE.txt","w")
    Wfile.write(repr(maxV))
    Wfile.close();
    print(maxV)

