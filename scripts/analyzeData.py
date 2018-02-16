import sys
import numpy as np
import math

#funcion for writing data
def writeToFile(X,Y,FILE):
        meanY = np.mean(Y);
        sqrtN = pow(len(Y),0.5);
        deltaY = np.std(m)/sqrtN;
        if math.isnan(deltaE):
            deltaE = float('0');
        if math.isnan(deltaM):
            deltaM = float('0');
        if math.isnan(deltaB):
            deltaB = float('0');
        if math.isnan(deltaD):
            deltaD = float('0');
        if math.isnan(deltaX):
            deltaX = float('0');
        if math.isnan(deltaR):
            deltaR = float('0');
        EF.write(repr(T)+"    "+repr(meanE)+"    "+repr(deltaE)+"    "+repr(N)+"\n")
        MF.write(repr(T)+"    "+repr(meanM)+"    "+repr(deltaM)+"    "+repr(N)+"\n")
        BF.write(repr(T)+"    "+repr(meanB)+"    "+repr(deltaB)+"    "+repr(N)+"\n")
        DF.write(repr(T)+"    "+repr(meanD)+"    "+repr(deltaD)+"    "+repr(N)+"\n")
        XF.write(repr(T)+"    "+repr(meanX)+"    "+repr(deltaX)+"    "+repr(N)+"\n")
        RF.write(repr(T)+"    "+repr(meanR)+"    "+repr(deltaR)+"    "+repr(N)+"\n")
        En[:]= []
        Mag[:]= []
        Bin [:]= []
        Dbdt[:]= []
        Xi[:]= []
        Rs[:]= []

#read raw data from file in ./output
#################################
# Format::
# 0      1      2      3      4      5      6            
# l      t      neqsw  neqcl  nsmsw  nsmcl  cold
# 7      8      9      10     11     12     13                
# E      E2     M      M2     M4     M2E    M4E
# 14     15     16     17     18     19     20     21                
# SX     SY     SZ     bin    dBdT   xi     rs     expFac
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

ind = np.lexsort((mat[:,21],mat[:,20],mat[:,19],mat[:,18],mat[:,17],mat[:,16],mat[:,15],mat[:,14],mat[:,13],mat[:,12],mat[:,11],mat[:,10],mat[:,9],mat[:,8],mat[:,7],mat[:,5],mat[:,4],mat[:,3],mat[:,2],mat[:,6],mat[:,1],mat[:,0]));

mat = mat[ind]

L=mat[0,0];
T=mat[0,1];
Neq_sw = mat[0,2];


sumlist = mat[0,:];

N = float('0.0');

#open files for writing
#separate files for different systemsizes

EF = open("./foutput/en/"+str(int(L))+"_"+fName+".dat","w")
MF = open("./foutput/mag/"+str(int(L))+"_"+fName+".dat","w")
BF = open("./foutput/bin/"+str(int(L))+"_"+fName+".dat","w")
newBF = open("./foutput/bin/"+str(int(L))+"_"+fName+"new.dat","w")
DF = open("./foutput/dbdt/"+str(int(L))+"_"+fName+".dat","w")
newDF = open("./foutput/dbdt/"+str(int(L))+"_"+fName+"new.dat","w")
XF = open("./foutput/xi/"+str(int(L))+"_"+fName+".dat","w")
newXF = open("./foutput/xi/"+str(int(L))+"_"+fName+"new.dat","w")
RF = open("./foutput/rs/"+str(int(L))+"_"+fName+".dat","w")
newRF = open("./foutput/rs/"+str(int(L))+"_"+fName+"new.dat","w")

TOL = float('0.00000000001');
for i in range(mat.shape[0]):
    #if new value of L, make new outputfile
    if(TOL < abs(mat[i,0] - L)):
        writeToFile(En,Mag,Bin,Dbdt,Xi,Rs,EF,MF,BF,DF,XF,RF,N,T,Neq)
        N=0;
        L = float(mat[i,0])
        T = float(mat[i,1])
        Neq = float(mat[i,8])
        EF = open("./foutput/en/"+str(int(L))+"_"+fName+".dat","w")
        MF = open("./foutput/mag/"+str(int(L))+"_"+fName+".dat","w")
        BF = open("./foutput/bin/"+str(int(L))+"_"+fName+".dat","w")
        DF = open("./foutput/dbdt/"+str(int(L))+"_"+fName+".dat","w")
        XF = open("./foutput/xi/"+str(int(L))+"_"+fName+".dat","w")
        RF = open("./foutput/rs/"+str(int(L))+"_"+fName+".dat","w")
    elif(TOL < abs(mat[i,1] - T)):
        writeToFiles(En,Mag,Bin,Dbdt,Xi,Rs,EF,MF,BF,DF,XF,RF,N,T,Neq)
        N=0;
        T = float(mat[i,1])
        Neq = float(mat[i,8])
    #normally just append to lists
    En.append(mat[i,2])
    Mag.append(mat[i,3])
    Bin.append(mat[i,4])
    Dbdt.append(mat[i,5])
    Xi.append(mat[i,6])
    Rs.append(mat[i,7])
    NeqSw.append(mat[i,8])
    NeqCl.append(mat[i,9])
    N = N + float('1.0')
writeToFiles(En,Mag,Bin,Dbdt,Xi,Rs,EF,MF,BF,DF,XF,RF,N,T,Neq)
