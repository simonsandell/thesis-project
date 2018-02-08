import subprocess

list4 = [];
list8 = [];
list16 = [];
list32 = [];
list64 = [];

lists = { 4:list4,
        8:list8,
        16:list16,
        32:list32,
        64:list64
        }

directory = "/home/simsan/exjobb/modular/maxE/";
for filename in os.listdir(directory):
    strL = filename.rsplit("_")
    L = int(strL[0]);
    fpath = directory + filename;
    Rfile = open(directory+filename,"r")
    val = float(Rfile.read())
    lists[L].append(val);

subprocess.call(["rm","-r",directory])
subprocess.call(["mkdir",directory])
for l in lists:
    maxV = 0;
    for v in lists[l]:
        if (abs(v) > abs(maxV)):
            maxV = v;
    Wfile = open(directory + str(l) + "_maxE.txt","w")
    Wfile.write(repr(maxV))

