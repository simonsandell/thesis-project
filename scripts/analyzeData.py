import sys
import numpy as np
import math

#funcion for writing data
def writeToFile(X,Y,FILE):
        meanY = np.mean(Y);
        sqrtN = pow(len(Y),0.5);
        deltaY = np.std(m)/sqrtN;
        if math.isnan(deltaY):
            deltaY = float('0');
        FILE.write(repr(X)+"    "+repr(meanY)+"    "+repr(deltaY)+"    "+repr(len(N))+"\n")
        Y[:]= []

def calcAvg(mat,i,istart,FileList):
    N = i - istart;
    T = mat[istart,1];
    L = mat[istart,0];
    iend = i -1;
    expFac = np.mean(mat[istart:iend,21]);
    E = np.mean(mat[istart:iend,21]);
    E2 = np.mean(mat[istart:iend,21]);
    M = np.mean(mat[istart:iend,21]);
    M2 = np.mean(mat[istart:iend,21]);
    M4 = np.mean(mat[istart:iend,21]);
    M2E = np.mean(mat[istart:iend,21]);
    M4E = np.mean(mat[istart:iend,21]);
    
    SX = np.mean(mat[istart:iend,21]);
    SY = np.mean(mat[istart:iend,21]);
    SZ = np.mean(mat[istart:iend,21]);

    B = np.mean(mat[istart:iend,21]);
    dBdT = np.mean(mat[istart:iend,21]);
    xi = np.mean(mat[istart:iend,21]);
    rs = np.mean(mat[istart:iend,21]);
    
    calcB = expFac*E/pow(E2,2);
    calcdBdT =  expFac*M4E*M2 + M4*M2*E -2.0*expFac*M4*M2E;
    calcdBdT = calcdBdT/(T*T*M2*M2*M2);
    calcxi = (M2/ expFac) - M*M/(expFac*expFac);
    calcxi = calcxi/(L*L*L*T);
    calcrs = -E -SX/T - SY/T - SZ/T;
    calcrs = calcrs/(3.0*L*L*expFac);
    for F in FileList:
        F.write(

#
#read raw data from file in ./output
##########################################################
# Format::
# 0      1      2      3      4      5      6            
# L      T      neqsw  neqcl  nsmsw  nsmcl  cold
#
# 7      8      9      10     11     12     13                
# E      E2     M      M2     M4     M2E    M4E
#
# 14     15     16     17     18     19     20     21                
# SX     SY     SZ     bin    dBdT   xi     rs     expFac
arguments = sys.argv
fName = arguments[1]
data0 = open("./output/" + fName,"r")
vals = []
#load data and form array
for ln in data0:
    strlist = ln.rsplit(" ")
    strlist = [x for x in strlist if not (x=="\n")]
    fllist = [float(x) for x in strlist] 
    vals.append(fllist)
mat = np.array(vals)

#Sort input data    
ind = np.lexsort((mat[:,21],mat[:,20],mat[:,19],mat[:,18],mat[:,17],mat[:,16],mat[:,15],mat[:,14],mat[:,13],mat[:,12],mat[:,11],mat[:,10],mat[:,9],mat[:,8],mat[:,7],mat[:,5],mat[:,4],mat[:,3],mat[:,2],mat[:,6],mat[:,1],mat[:,0]));
mat = mat[ind]

#form averages and print to file
L=mat[0,0];
T=mat[0,1];
Neq_sw = mat[0,2];

collection = [mat[0,:]];

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

FileList = [EF,MF,BF,newBF,DF,newDF,XF,newXF,RF,newRF]

TOL = float('0.00000000001');
ifirst = 0;
for i in range(mat.shape[0]):
    #if new value of L, make new outputfile
    if(TOL < abs(mat[i,0] - L)):
        calcAvg(mat,i,ifirst);
        writeToFile(X,Y,FILE);
        writeToFile(T,sumlist[7],EF);
        writeToFile(T,sumlist[9],EF);
        writeToFile(T,sumlist[9],EF);
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
    N = N + float('1.0')
writeToFiles(En,Mag,Bin,Dbdt,Xi,Rs,EF,MF,BF,DF,XF,RF,N,T,Neq)
