import subprocess
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



#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
#Neqrange = [65536,131072,262144,524288,1048576]
#nequilRun(4,2.2,10,Neqrange)
#temperatureRun();
Trange = [2.1,2.12,2.14,2.16,2.18,2.2,2.22,2.24,2.26,2.28,2.3]
histRun(4,Trange,100)
