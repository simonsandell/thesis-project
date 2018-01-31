import subprocess
def temperatureRun(Lrange,Trange,N,N_equil,N_samples):
    for i in range(N):
        for t in Trange:
            for L in Lrange:
                subprocess.call(["./a.out"+ " " +str(L)+ " " +str(t)+ " 0 " +str(N_equil) + " "+ str(N_samples)+" >> "+" ./output/temperatureRun"],shell=True)
# histInput : L Neq Nsamp M0 T0 T1 T2 ...
def histRun(L,Neq,Nsamp,initM,Temps,N):
    T_str = ""
    for t in Temps:
        T_str = T_str + str(t) + " "
    for i in range(N):
        subprocess.call(["./a.out "+L + Neq + Nsamp +initM + T_str + ">>  ./output/histRun"],shell=True)

def nequilRun(L,T,Nruns,Neqrange):
    N_samples =1;
    for i in range(Nruns):
        for n in Neqrange:
            subprocess.call(["./a.out "+str(L)+" "+str(n)+" 1 0 "+str(T)+" >>  ./output/nequil0"],shell=True)
            subprocess.call(["./a.out "+str(L)+" "+str(n)+" 1 1 "+str(T)+" >>  ./output/nequil1"],shell=True)


def getTrange(Tstart,Tend,Tnum):
    dt = (Tend - Tstart)/(Tnum)
    ret = []
    for i in range(Tnum):
        ret.append(Tstart + i*dt)
    return ret
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#


Trange = getTrange(1.8,2.5,10)
#Trange = getTrange(2.1,2.3,30)
N_equil = 300
N_samples = N_equil
Lrange = [4,8,16]
N = 20

Neqrange = [4,16,64,256,1042,4168]
nequilRun(4,2.20429,N,Neqrange)
nequilRun(8,2.20429,N,Neqrange)
nequilRun(16,2.20429,N,Neqrange)
#temperatureRun(Lrange,Trange,N,N_equil,N_samples);
#histRun("4",Trange,N)
#histRun(8,Trange,N)
#histRun(16,Trange,N)
