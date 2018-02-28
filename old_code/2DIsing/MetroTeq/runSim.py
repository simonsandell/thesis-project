import subprocess
import numpy as np


#compile
command = subprocess.run(["g++","ising2.cpp"],stderr=subprocess.PIPE)
output = command.stderr.decode('utf-8')
if( output != ""):
    print(output)
    exit(-1)
#ask if want to overwrite previous output
x = input("files in output/ will be overwritten. Enter asdf to continue\n")
if ( x != "asdf"):
    exit(0)

#run for different number of sweeps as the teq
N = 1000
for L in [2,4,8,16,32]:
    fM0 = open("output/M0_" + str(L) + ".dat","w")
    fM1 = open("output/M1_" + str(L) + ".dat","w")
    for N_sweeps in [2,4,8,16,32,64,128,256]:
        t1 = []
        t0 = []
        m1 = []
        m0 = []
        for N in range(N):
            runM0 = subprocess.run(["./a.out",str(L),str(N_sweeps),str(0)],stdout=subprocess.PIPE)
            outM0 = runM0.stdout.decode('utf-8')
            runM1 = subprocess.run(["./a.out",str(L),str(N_sweeps),str(1)],stdout=subprocess.PIPE)
            outM1 = runM1.stdout.decode('utf-8')
            m0v = outM0.rsplit(" ")
            m1v = outM1.rsplit(" ")
            t0.append(float(m0v[0]))
            t1.append(float(m1v[0]))
            m0.append(float(m0v[1]))
            m1.append(float(m1v[1]))
        fM0.write(str(np.mean(t0)) + " " + str(np.mean(m0))+ " " + str(np.std(t0)) + " " + str((np.std(m0)/(N** 0.5))) +  "\n")
        fM1.write(str(np.mean(t1)) + " " + str(np.mean(m1))+ " " + str(np.std(t1)) + " " + str((np.std(m1)/(N** 0.5))) +  "\n")
    fM0.close()
    fM1.close()
    print("done with " + str(L))

done = subprocess.run(["notify-send","Metropolis Teq simulation finished"])
