import subprocess
import numpy as np

#compile
comp = subprocess.run(["g++","ising2.cpp"],stderr=subprocess.PIPE,stdout=subprocess.PIPE)
print( comp.stdout.decode('utf-8'))
fail = comp.stderr.decode('utf-8')
if ( fail != ""):
    print(fail)
    exit(-1)

#check if want to save previous output
x = input("files in /output/ will be overwritten. Type asdf to continue")
if x != "asdf":
    exit(0)

Tc = 2.26918531421
#Trange = [Tc-0.01,Tc,Tc+0.01,Tc+0.02,Tc+0.03,Tc+0.04,Tc+0.05,Tc+0.06,Tc+0.07,Tc+0.08]
Lrange = [4,8,16,32]
Trange = [2.10,2.12,2.14,2.16,2.18,2.20,2.22,2.24,2.26,2.28,2.30,2.32,2.34,2.36,2.38,2.40,2.42,2.44,2.46,2.48,2.50]
N_samples = 100;
for L in Lrange:
    print(L)
    f_bin = open("output/binder" + str(L) + ".dat","w")
    f_dbdt = open("output/dbdt" + str(L) + ".dat","w")
    f_xi = open("output/xi" + str(L) + ".dat","w")
    for T in Trange:
        print(T)
        binder = []
        dbdt = []
        xi = []
        for n in range(N_samples):
            test = subprocess.run(["./a.out",str(L),str(T)],stdout=subprocess.PIPE)
            output = test.stdout.decode('utf-8')
            vals = output.rsplit(" ")
            binder.append(float(vals[0]))
            dbdt.append(float(vals[1]))
            xi.append(float(vals[2]))
        # calculate average, sigma and write to file
        avgBin = np.mean(binder)
        avgDbdt = np.mean(dbdt)
        avgXi = np.mean(xi)
        sigmaBin = np.std(binder)
        sigmaDbdt = np.std(dbdt)
        sigmaXi = np.std(xi)
        deltaBin = sigmaBin/(N_samples ** 0.5)
        deltaDbdt = sigmaDbdt/(N_samples ** 0.5)
        deltaXi = sigmaXi/(N_samples ** 0.5)

        f_bin.write(str(T) + " " + str(avgBin) + " " + str(deltaBin) + "\n")
        f_dbdt.write(str(T) + " " + str(avgDbdt) + " " + str(deltaDbdt) + "\n")
        f_xi.write(str(T) + " " + str(avgXi) + " " + str(deltaXi) + "\n")
    f_bin.close()
    f_dbdt.close()
    f_xi.close()
asdf= subprocess.run(["notify-send","Metropolis Ising 2d sim finished"])
