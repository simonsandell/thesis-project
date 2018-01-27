import sys
import numpy as np
import math
#funcion for writing data
def writeToFiles(En,Mag,Bin,Dbdt,Xi,EF,MF,M_teq,BF,DF,XF,N,T,Neq):
        meanE = np.mean(En);
        meanM = np.mean(Mag);
        meanB = np.mean(Bin);
        meanD = np.mean(Dbdt);
        meanX = np.mean(Xi);
        deltaE = np.std(En)/(N**0.5);
        deltaM = np.std(Mag)/(N**0.5);
        deltaB = np.std(Bin)/(N**0.5);
        deltaD = np.std(Dbdt)/(N**0.5);
        deltaX = np.std(Xi)/(N**0.5);
        if math.isnan(deltaE):
            deltaE = 0;
        if math.isnan(deltaM):
            deltaM = 0;
        if math.isnan(deltaB):
            deltaB = 0;
        if math.isnan(deltaD):
            deltaD = 0;
        if math.isnan(deltaX):
            deltaX = 0;
        EF.write(str(T)+" "+str(meanE)+" "+str(deltaE)+"\n")
        MF.write(str(T)+" "+str(meanM)+" "+str(deltaM)+"\n")
        M_teq.write(str(Neq)+" "+str(meanM)+" "+str(deltaM)+"\n")
        BF.write(str(T)+" "+str(meanB)+" "+str(deltaB)+"\n")
        DF.write(str(T)+" "+str(meanD)+" "+str(deltaD)+"\n")
        XF.write(str(T)+" "+str(meanX)+" "+str(deltaX)+"\n")
        En[:]= []
        Mag[:]= []
        Bin [:]= []
        Dbdt[:]= []
        Xi[:]= []
        N = 0

#read raw data from file in ./output

arguments = sys.argv
fName = arguments[1]
data0 = open("./output/" + fName,"r")
vals = []
for ln in data0:
    strlist = ln.rsplit(" ")
    strlist = [x for x in strlist if not (x=="\n")]
    fllist = [float(x) for x in strlist] 
    vals.append(fllist)

#sort by L, T, N_equil in that order    
mat = np.array(vals)
ind = np.lexsort((mat[:,6],mat[:,5],mat[:,4],mat[:,3],mat[:,2],mat[:,7],mat[:,1],mat[:,0]))
mat = mat[ind]
#mat = mat[np.argsort(mat.A[:,0],-1,'mergesort')]
#mat = mat[np.argsort(mat.A[:,1],-1,'mergesort')]
#mat = mat[np.argsort(mat.A[:,7],-1,'mergesort')]

L=mat[0,0];
T=mat[0,1];
Neq = mat[0,7];
En=[];
Mag=[];
Bin=[];
Dbdt=[];
Xi=[];
N = 0;

#open files for writing
#separate files for different systemsizes

EF = open("./foutput/en/"+str(int(L))+"_"+fName+".dat","w")
MF = open("./foutput/mag/"+str(int(L))+"_"+fName+".dat","w")
M_teq = open("./foutput/teq/"+str(int(L))+"_"+fName+".dat","w")
BF = open("./foutput/bin/"+str(int(L))+"_"+fName+".dat","w")
DF = open("./foutput/dbdt/"+str(int(L))+"_"+fName+".dat","w")
XF = open("./foutput/xi/"+str(int(L))+"_"+fName+".dat","w")

TOL = 10e-10
for i in range(mat.shape[0]):
    #if new value of L, make 
    if(TOL < abs(mat[i,0] - L)):
        writeToFiles(En,Mag,Bin,Dbdt,Xi,EF,MF,M_teq,BF,DF,XF,N,T,Neq)
        L = mat[i,0]
        T = mat[i,1]
        Neq = mat[i,7]
        EF = open("./foutput/en/"+str(int(L))+"_"+fName+".dat","w")
        MF = open("./foutput/mag/"+str(int(L))+"_"+fName+".dat","w")
        M_teq = open("./foutput/teq/"+str(int(L))+"_"+fName+".dat","w")
        BF = open("./foutput/bin/"+str(int(L))+"_"+fName+".dat","w")
        DF = open("./foutput/dbdt/"+str(int(L))+"_"+fName+".dat","w")
        XF = open("./foutput/xi/"+str(int(L))+"_"+fName+".dat","w")
    elif(TOL < abs(mat[i,1] - T)):
        writeToFiles(En,Mag,Bin,Dbdt,Xi,EF,MF,M_teq,BF,DF,XF,N,T,Neq)
        T = mat[i,1]
        Neq = mat[i,7]
    elif (TOL < abs(mat[i,7] - Neq)):
        writeToFiles(En,Mag,Bin,Dbdt,Xi,EF,MF,M_teq,BF,DF,XF,N,T,Neq)
        Neq = mat[i,7]
    #normally just append to lists
    En.append(mat[i,2])
    Mag.append(mat[i,3])
    Bin.append(mat[i,4])
    Dbdt.append(mat[i,5])
    Xi.append(mat[i,6])
    N = N + 1   
writeToFiles(En,Mag,Bin,Dbdt,Xi,EF,MF,M_teq,BF,DF,XF,N,T,Neq)
