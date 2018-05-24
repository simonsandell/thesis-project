import os
import sys
res = [];
for direc,subdir,files in os.walk(sys.argv[1]):
    dop = False;
    for f in files:
        if ".dat" in f:
            dop = True;
    if dop:
        res.append(direc);

of = open("./foutput_struct.fst","w");
for ln in res:
    of.write(ln+"\n");

