import subprocess
def temperatureRun(Lrange,Trange,N,N_equil,N_samples):
    for i in range(N):
        for t in Trange:
            for L in Lrange:
                subprocess.call(["./a.out"+ " " +str(L)+ " " +str(t)+ " 1 " +str(N_equil) + " "+ str(N_samples)+" >> "+" ./output/temperatureRun"],shell=True)

# histInput : L Neq Nsamp M0 T0 T1 T2 ...
def histRun(L,Neq,Nsamp,initM,Temps,N):
    T_str = ""
    for t in Temps:
        T_str = T_str + str(t) + " "
    for i in range(N):
        inputstr = "./a.out " + L +" "+ Neq +" "+ Nsamp +" "+ initM +" "+ T_str + ">>  ./output/rhistRun"
        print(inputstr)
        subprocess.call([inputstr],shell=True)

def nequilRun(L,T,Nruns,Neqrange):
    N_samples =1;
    for i in range(Nruns):
        for n in Neqrange:
            subprocess.call(["./a.out "+L+" "+str(n)+" 1 0 "+T+" >>  ./output/nequil0"],shell=True)
            subprocess.call(["./a.out "+L+" "+str(n)+" 1 1 "+T+" >>  ./output/nequil1"],shell=True)


def getTrange(Tstart,Tend,Tnum):
    dt = (Tend - Tstart)/(Tnum)
    ret = []
    for i in range(Tnum):
        ret.append(Tstart + i*dt)
    return ret
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# ---  Params  ----
#Trange = getTrange(1.8,2.5,10)
Trange = getTrange(2.2,2.22,30)
N_equil = "1000"
N_samples = "2000"
Lrange = [4,8,16]
N = 100

# def nequilRun(L,T,Nruns,Neqrange):
#Neqrange4 = [16,32,64,128,256,512,1042,2048,4136,8272]
#Neqrange8 = [64,128,256]
#Neqrange16 = [128,256,512,1042]
#nequilRun("4","2.20429",N2,Neqrange4)
#nequilRun("8","2.20429",N,Neqrange4)
#nequilRun("16","2.20429",N,Neqrange4)
temperatureRun(Lrange,Trange,N,N_equil,N_samples);

# def histRun(L,Neq,Nsamp,initM,Temps,N):
#histRun("4",N_equil,N_samples,"1",Trange,N)
#histRun("8",N_equil,N_samples,"1",Trange,N)
#histRun("16",N_equil,N_samples,"1",Trange,N)
