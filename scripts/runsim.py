import subprocess
import os
dl = os.path.dirname(os.path.realpath(__file__)).rsplit("/")
dn = dl[len(dl)-1]
print(dl)
print(dn)
dir_list = os.getcwd().rsplit("/")
dir_name = dir_list[len(dir_list)-1]
print(dir_list)
print(dir_name)
def temperatureRun():
    Tstart = 1
    Tend = 3
    dt = (Tend -Tstart)/20
    
    Lrange = [4]
    
    N_equil = 2000;
    N_samples = N_equil;
    
    for i in range(100):
        T = Tstart
        for t in range(20):
            T = T + dt;
            for L in Lrange:
                subprocess.call(["./a.out"+ " " +str(L)+ " " +str(T)+ " " +str(1)+ " " +str(N_equil) + " "+ str(N_samples)+" >> "+" ./output/temperatureRun"],shell=True)


def nequilRun(L,T,Nruns,Neqrange):
    N_samples =1;
    for i in range(Nruns):
        for n in Neqrange:
            subprocess.call(["./a.out"+" "+str(L)+" "+str(T)+" 0 "+str(n)+" 1 >>  ./output/nequil"+str(L)],shell=True)
            subprocess.call(["./a.out"+" "+str(L)+" "+str(T)+" 1 "+str(n)+" 1 >>  ./output/nequil"+str(L)],shell=True)



#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
#Neqrange = [65536,131072,262144,524288,1048576]
#nequilRun(4,2.2,10,Neqrange)
#temperatureRun();
