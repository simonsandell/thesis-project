import subprocess
def temperatureRun(Lrange,Trange,N,N_equil,N_samples):
    for i in range(N):
        for t in Trange:
            for L in Lrange:
                subprocess.call(["./a.out"+ " " +str(L)+ " " +str(t)+ " 0 " +str(N_equil) + " "+ str(N_samples)+" >> "+" ./output/temperatureRun"],shell=True)

def histRun(L,Temps,N):
    T_str = ""
    for t in Temps:
        T_str = T_str + str(t) + " "
    for i in range(N):
        subprocess.call(["./a.out"+" "+str(L)+" " + T_str + ">>  ./output/histRun"],shell=True)

def nequilRun(L,T,Nruns,Neqrange):
    N_samples =1;
    for i in range(Nruns):
        for n in Neqrange:
            subprocess.call(["./a.out"+" "+str(L)+" "+str(T)+" 0 "+str(n)+" 1 >>  ./output/nequil"],shell=True)
            subprocess.call(["./a.out"+" "+str(L)+" "+str(T)+" 1 "+str(n)+" 1 >>  ./output/nequil"],shell=True)


def getTrange(Tstart,Tend,Tnum):
    dt = (Tend - Tstart)/(Tnum)
    ret = []
    for i in range(Tnum):
        ret.append(Tstart + i*dt)
    return ret
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#


Trange = getTrange(1.5,2.9,30)
N_equil = 300
N_samples = N_equil
Lrange = [4,8,16]
N = 50

#Neqrange = [65536,131072,262144,524288,1048576]
#nequilRun(4,2.2,10,Neqrange)
temperatureRun(Lrange,Trange,N,N_equil,N_samples);
#histRun(4,Trange,N)
#histRun(8,Trange,N)
#histRun(16,Trange,N)
