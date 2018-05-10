import os
import sys
import numpy as np
import pickler

# N_vals = 22 for 3DXY, 19 for Ising3D
def loadData(path,N_vals):
    data = [];
    datafile = open(path,"r");
    i = 0;
    for ln in datafile:
        i = i+1;
        if not (('#' in ln) or ('WORLD' in ln) or ('SEED' in ln) or ('aprun' in ln)):
            strlist = ln.rsplit(" ");
            strlist = [x for x in strlist if not (x== "\n")];
            try:
                fllist = [float(x) for x in strlist];
                if (len(fllist) != N_vals):
                    print('bad line at row ' + str(1 + i));
                data.append(fllist);
            except:
                print(fName);
                print(len(strlist));
                print('bad line at row ' + str(1 + i));
                load_failed = True;
    return data;

path = sys.argv[1];
model = sys.argv[2];
saveName = sys.argv[3];
if (sys.argv[2] == "3DXY"):
    nvals = 22;
else:
    nvals = 19;

arrarr = [];
i = 0;
nfils = len(os.listdir(path));
for filename in os.listdir(path):
    i+=1;
    print("("+str(i)+"/"+str(nfils)+") - "+filename);
    if (os.path.isfile(os.path.join(path,filename))):
        arrarr.extend(loadData(os.path.join(path,filename),nvals));
npmat = np.array(arrarr);
ind = np.lexsort((npmat[:,1],npmat[:,0]));
npmat = npmat[ind];
pickler.saveData(npmat,sys.argv[2]+saveName);
