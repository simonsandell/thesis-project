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
N = 100

Trange = [2.10,2.12,2.14,2.16,2.18,2.20,2.22,2.24,2.26,2.26918531421,2.28,2.30,2.32,2.34,2.36,2.38,2.40,2.42,2.44,2.46,2.48,2.50]
N_temp = len(Trange)

binder = np.zeros((N_temp,N))
dbdt = np.zeros((N_temp,N))
xi= np.zeros((N_temp,N))
dB= np.zeros((N_temp,N))
dDB= np.zeros((N_temp,N))
dXi= np.zeros((N_temp,N))

vals = []
for L in [4,8,16,32]:
    fB = open("output/binder_" + str(L) + ".dat","w")
    fDB = open("output/dbdt_" + str(L) + ".dat","w")
    fXi = open("output/xi_" + str(L) + ".dat","w")
    for k in range(N):
        command = subprocess.run(["./a.out",str(L)],stdout=subprocess.PIPE)
        output = command.stdout.decode('utf-8')
        vals = output.rsplit(" ")
        for i in range(N_temp):
            binder[i][k] = vals[i]
            dbdt[i][k] = vals[i+N_temp]
            xi[i][k] = vals[i + 2*N_temp]
    for i in range(N_temp):
        bmean = str(np.mean(binder[i]))
        bdel = str(np.std(binder[i])/(N ** 0.5))
        dbdtmean = str(np.mean(dbdt[i]))
        dbdtdel = str(np.std(dbdt[i])/(N ** 0.5))
        ximean = str(np.mean(xi[i]))
        xidel = str(np.std(xi[i])/(N ** 0.5))
        Tstr = str(Trange[i])
        fB.write(Tstr + " " + bmean + " " + bdel + "\n")
        fDB.write(Tstr + " " + dbdtmean + " " + dbdtdel + "\n")
        fXi.write(Tstr + " " + ximean + " " + xidel + "\n")
    fB.close()
    fDB.close()
    fXi.close()
    print("done with " + str(L) + "\n")
asdf = subprocess.run(["notify-send","runWolff.py finished"])
