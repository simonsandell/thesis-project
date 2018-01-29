import subprocess
def temperatureRun(Lrange,Trange,N):
    
    N_equil = 2000;
    N_samples = N_equil;
    
    for i in range(N):
        for t in Trange:
            for L in Lrange:
                subprocess.call(["./a.out"+ " " +str(L)+ " " +str(T)+ " " +str(1)+ " " +str(N_equil) + " "+ str(N_samples)+" >> "+" ./output/temperatureRun"],shell=True)

def histRun(L,Temps,N):
    T_str = ""
    for t in Temps:
        T_str = T_str + str(t) + " "
    for i in range(N):
        subprocess.call(["./a.out"+" "+str(L)+" " + T_str + ">>  ./output/histRun"+str(L)],shell=True)

def nequilRun(L,T,Nruns,Neqrange):
    N_samples =1;
    for i in range(Nruns):
        for n in Neqrange:
            subprocess.call(["./a.out"+" "+str(L)+" "+str(T)+" 0 "+str(n)+" 1 >>  ./output/nequil"+str(L)],shell=True)
            subprocess.call(["./a.out"+" "+str(L)+" "+str(T)+" 1 "+str(n)+" 1 >>  ./output/nequil"+str(L)],shell=True)


def getTrange(Tstart,Tend,Tnum):
    dt = (Tend - Tstart)/(Tnum)
    ret = []
    for i in range(Tnum):
        ret.append(Tstart + i*dt)
    return ret
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
#Neqrange = [65536,131072,262144,524288,1048576]
#nequilRun(4,2.2,10,Neqrange)
#temperatureRun();
Trange = getTrange(1.5,2.9,20)
histRun(8,Trange,200)
