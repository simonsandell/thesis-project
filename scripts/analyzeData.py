import decimal
import sys
import numpy as np
import math

#funcion for writing data
def writeToFiles(En,Mag,Bin,Dbdt,Xi,Rs,EF,MF,BF,DF,XF,RF,N,T,Neq):
        meanE = np.mean(En);
        meanM = np.mean(Mag);
        meanB = np.mean(Bin);
        meanD = np.mean(Dbdt);
        meanX = np.mean(Xi);
        meanR = np.mean(Rs);
        sqrtN = N.sqrt();
        deltaE = np.std(En)/sqrtN;
        deltaM = np.std(Mag)/sqrtN;
        deltaB = np.std(Bin)/sqrtN;
        deltaD = np.std(Dbdt)/sqrtN;
        deltaX = np.std(Xi)/sqrtN;
        deltaR = np.std(Rs)/sqrtN;
        if math.isnan(deltaE):
            deltaE = decimal.Decimal('0');
        if math.isnan(deltaM):
            deltaM = decimal.Decimal('0');
        if math.isnan(deltaB):
            deltaB = decimal.Decimal('0');
        if math.isnan(deltaD):
            deltaD = decimal.Decimal('0');
        if math.isnan(deltaX):
            deltaX = decimal.Decimal('0');
        if math.isnan(deltaR):
            deltaR = decimal.Decimal('0');
        EF.write(str(T)+"    "+str(meanE)+"    "+str(deltaE)+"    "+str(N)+"\n")
        MF.write(str(T)+"    "+str(meanM)+"    "+str(deltaM)+"    "+str(N)+"\n")
        BF.write(str(T)+"    "+str(meanB)+"    "+str(deltaB)+"    "+str(N)+"\n")
        DF.write(str(T)+"    "+str(meanD)+"    "+str(deltaD)+"    "+str(N)+"\n")
        XF.write(str(T)+"    "+str(meanX)+"    "+str(deltaX)+"    "+str(N)+"\n")
        RF.write(str(T)+"    "+str(meanR)+"    "+str(deltaR)+"    "+str(N)+"\n")
        En[:]= []
        Mag[:]= []
        Bin [:]= []
        Dbdt[:]= []
        Xi[:]= []
        Rs[:]= []

#read raw data from file in ./output
#################################
# Format::
# 0      1      2      3      4      5      6      7      8      9      10      11      12      
# L      T      E      M      B      dBdT   xi     rs     eqsw   eqcl   smsw    smcl    cold

arguments = sys.argv
fName = arguments[1]
data0 = open("./output/" + fName,"r")
vals = []
for ln in data0:
    strlist = ln.rsplit(" ")
    strlist = [x for x in strlist if not (x=="\n")]
    fllist = [decimal.Decimal(x) for x in strlist] 
    vals.append(fllist)

#sort by L, T, N_equil in that order    
mat = np.array(vals)
ind = np.lexsort((mat[:,12],mat[:,11],mat[:,10],mat[:,9],mat[:,7],mat[:,6],mat[:,5],mat[:,4],mat[:,3],mat[:,2],mat[:,8],mat[:,1],mat[:,0]))

mat = mat[ind]

L=mat[0,0];
T=mat[0,1];
Neq = mat[0,7];
En=[];
Mag=[];
Bin=[];
Dbdt=[];
Xi=[];
Rs=[];
NeqSw=[];
NeqCl=[];
N = decimal.Decimal('0.0');

#open files for writing
#separate files for different systemsizes

EF = open("./foutput/en/"+str(int(L))+"_"+fName+".dat","w")
MF = open("./foutput/mag/"+str(int(L))+"_"+fName+".dat","w")
BF = open("./foutput/bin/"+str(int(L))+"_"+fName+".dat","w")
DF = open("./foutput/dbdt/"+str(int(L))+"_"+fName+".dat","w")
XF = open("./foutput/xi/"+str(int(L))+"_"+fName+".dat","w")
RF = open("./foutput/rs/"+str(int(L))+"_"+fName+".dat","w")

TOL = decimal.Decimal('0.0000000000001');
for i in range(mat.shape[0]):
    #if new value of L, make new outputfile
    if(TOL < abs(mat[i,0] - L)):
        writeToFiles(En,Mag,Bin,Dbdt,Xi,Rs,EF,MF,BF,DF,XF,RF,N,T,Neq)
        N=0;
        L = decimal.Decimal(mat[i,0])
        T = decimal.Decimal(mat[i,1])
        Neq = decimal.Decimal(mat[i,8])
        EF = open("./foutput/en/"+str(int(L))+"_"+fName+".dat","w")
        MF = open("./foutput/mag/"+str(int(L))+"_"+fName+".dat","w")
        BF = open("./foutput/bin/"+str(int(L))+"_"+fName+".dat","w")
        DF = open("./foutput/dbdt/"+str(int(L))+"_"+fName+".dat","w")
        XF = open("./foutput/xi/"+str(int(L))+"_"+fName+".dat","w")
        RF = open("./foutput/rs/"+str(int(L))+"_"+fName+".dat","w")
    elif(TOL < abs(mat[i,1] - T)):
        writeToFiles(En,Mag,Bin,Dbdt,Xi,Rs,EF,MF,BF,DF,XF,RF,N,T,Neq)
        N=0;
        T = decimal.Decimal(mat[i,1])
        Neq = decimal.Decimal(mat[i,8])
    #normally just append to lists
    En.append(mat[i,2])
    Mag.append(mat[i,3])
    Bin.append(mat[i,4])
    Dbdt.append(mat[i,5])
    Xi.append(mat[i,6])
    Rs.append(mat[i,7])
    NeqSw.append(mat[i,8])
    NeqCl.append(mat[i,9])
    N = N + decimal.Decimal('1.0')
writeToFiles(En,Mag,Bin,Dbdt,Xi,Rs,EF,MF,BF,DF,XF,RF,N,T,Neq)
