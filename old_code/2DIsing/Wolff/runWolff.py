import subprocess
import numpy as np


#compile 
command = subprocess.run(["g++","wolffnonrecursive.cpp"],stderr=subprocess.PIPE)
errors = command.stderr.decode('utf-8')
if (errors != ""):
    print(errors)
    exit(-1)
#ask if want to overwrite files
x = input("files in output/ will be overwritten. Enter asdf to continue")
if (x != "asdf"):
    exit(0)

#do runs N times
binder = []
dbdt = []
xi = []

Tc = 2.26918531421
#Trange = [Tc-0.01,Tc,Tc+0.01,Tc+0.02,Tc+0.03,Tc+0.04,Tc+0.05,Tc+0.06,Tc+0.07,Tc+0.08]
Trange = [2.10,2.12,2.14,2.16,2.18,2.20,2.22,2.24,2.26,2.28,2.30,2.32,2.34,2.36,2.38,2.40,2.42,2.44,2.46,2.48,2.50]
N = 100;
vals = []
for L in [4,8,16,32]:
    fB = open("output/binder_" + str(L) + ".dat","w")
    fDB = open("output/dbdt_" + str(L) + ".dat","w")
    fXi = open("output/xi_" + str(L) + ".dat","w")
    for T in Trange:
        for n in range(N):
            command = subprocess.run(["./a.out",str(L),str(T)],stdout=subprocess.PIPE)
            output = command.stdout.decode('utf-8')
            vals = output.rsplit(" ")
            binder.append(float(vals[0]))
            dbdt.append(float(vals[1]))
            xi.append(float(vals[2]))
        print(np.mean(binder))
        fB.write(str(T) + " " + str(np.mean(binder)) + " " + str(np.std(binder)/(N ** 0.5)) + "\n")
        fDB.write(str(T) + " " + str(np.mean(dbdt)) + " " + str(np.std(dbdt)/(N ** 0.5)) + "\n")
        fXi.write(str(T) + " " + str(np.mean(xi)) + " " + str(np.std(xi)/(N ** 0.5)) + "\n")
        binder = []
        dbdt = []
        xi = []
    fB.close()
    fDB.close()
    fXi.close()
    print("done with " + str(L) + "\n")
asdf = subprocess.run(["notify-send","Wolff simulation finished"])
