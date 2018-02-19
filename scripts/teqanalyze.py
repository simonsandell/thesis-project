import decimal
import sys
import numpy as np
import math

#funcion for writing data
def writeToFiles(Mag,M_teq,N,Neq):
        meanNeq = np.mean(Neq);
        meanM = np.mean(Mag);
        sqrtN = N.sqrt();
        deltaM = np.std(Mag)/sqrtN;
        if math.isnan(deltaM):
            deltaM = decimal.Decimal('0');
        M_teq.write(str(meanNeq)+"    "+str(meanM)+"    "+str(deltaM)+"    "+str(N)+"\n")
        Mag[:]= []
        Neq[:]= []
        
arguments = sys.argv
fName = arguments[1]
data0 = open("./teqoutput/" + fName,"r")
vals = []
for ln in data0:
    strlist = ln.rsplit(" ")
    strlist = [x for x in strlist if not (x=="\n")]
    fllist = [decimal.Decimal(x) for x in strlist] 
    vals.append(fllist)

#################################
# Format::
# 0      1      2      3      4      5      6      7      8      9      10      11      12      
# L      T      E      M      B      dBdT   xi     rs     eqsw   eqcl   smsw    smcl    cold
#sort by L, N_equil, T 
mat = np.array(vals)
ind = np.lexsort((mat[:,11],mat[:,10],mat[:,7],mat[:,6],mat[:,5],mat[:,4],mat[:,3],mat[:,2],mat[:,1],mat[:,9],mat[:,8],mat[:,12],mat[:,0]))
mat = mat[ind]

cold = decimal.Decimal(mat[0,12])
L=decimal.Decimal(mat[0,0])
Neq_sav = decimal.Decimal(mat[0,8])
Neq = [];
Mag=[];
N = decimal.Decimal('0.0');

#open files for writing
strFn = "./foutput/teq/" + str(int(cold)) + "_" + str(int(L)) + "_" + fName + ".dat"
M_teq = open(strFn,"w")
LTOL = decimal.Decimal('1');
TOL = decimal.Decimal('4') 
relTOL = decimal.Decimal('0.5')
for i in range(mat.shape[0]):
    #if new value of L or cold, make new outputfile
    if (abs(mat[i,12] - cold) > decimal.Decimal('0.1')):
        writeToFiles(Mag,M_teq,N,Neq)
        N = decimal.Decimal('0');
        L=decimal.Decimal(mat[i,0])
        Neq_sav = decimal.Decimal(mat[i,8])
        cold = decimal.Decimal(mat[i,12])
        strFn = "./foutput/teq/" + str(int(cold)) + "_" + str(int(L)) + "_" + fName + ".dat"
        M_teq = open(strFn,"w")
    elif(LTOL < abs(mat[i,0] - L)):
        writeToFiles(Mag,M_teq,N,Neq)
        N = decimal.Decimal('0');
        L = decimal.Decimal(mat[i,0])
        Neq_sav = decimal.Decimal(mat[i,8])
        strFn = "./foutput/teq/" + str(int(cold)) + "_" + str(int(L)) + "_" + fName + ".dat"
        M_teq = open(strFn,"w")
        #if new value of N_eq, take mean and write to file
    elif (relTOL < (decimal.Decimal('1.0')/(Neq_sav))*abs(mat[i,8] - Neq_sav)):
        writeToFiles(Mag,M_teq,N,Neq)
        N = decimal.Decimal('0');
        Neq_sav = decimal.Decimal(mat[i,8])
    Mag.append(mat[i,3])
    Neq.append(mat[i,8])
    Neq_sav = np.mean(Neq)
    N = N + decimal.Decimal('1.0')
writeToFiles(Mag,M_teq,N,Neq)
