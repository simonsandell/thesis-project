import decimal
import sys
import numpy as np
import math
# beta/nu ~ 0.5187891440
#funcion for writing data
def writeToFiles(L,Mag,M_teq,N,Neq):
        meanNeq = pow(L,-1.40)*np.mean(Neq);
        meanM = pow(L,0.44)*np.mean(Mag);
        sqrtN = pow(N,0.5);
        deltaM = np.std(Mag)/sqrtN;
        if math.isnan(deltaM):
            deltaM = float('0');
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
    fllist = [float(x) for x in strlist] 
    vals.append(fllist)

#################################
# Format::
# 0      1      2      3      4      5      6      7      8      9      10      11      12      
# L      T      E      M      B      dBdT   xi     rs     eqsw   eqcl   smsw    smcl    cold
#sort by L, N_equil, T 
mat = np.array(vals)
ind = np.lexsort((mat[:,11],mat[:,10],mat[:,7],mat[:,6],mat[:,5],mat[:,4],mat[:,3],mat[:,2],mat[:,1],mat[:,9],mat[:,8],mat[:,12],mat[:,0]))
mat = mat[ind]

cold = float(mat[0,12])
L=float(mat[0,0])
Neq_sav = float(mat[0,8])
Neq = [];
Mag=[];
N = float('0.0');

#open files for writing
strFn = "./foutput/teqmod/" + str(int(cold)) + "_" + str(int(L)) + "_" + fName + ".dat"
M_teq = open(strFn,"w")

TOL = float('4') 
relTOL = float('0.5')
for i in range(mat.shape[0]):
    #if new value of L or cold, make new outputfile
    if (abs(mat[i,12] - cold) > float('0.1')):
        writeToFiles(L,Mag,M_teq,N,Neq)
        N = float('0');
        L=float(mat[i,0])
        Neq_sav = float(mat[i,8])
        cold = float(mat[i,12])
        strFn = "./foutput/teqmod/" + str(int(cold)) + "_" + str(int(L)) + "_" + fName + ".dat"
        M_teq = open(strFn,"w")
    elif(TOL < abs(mat[i,0] - L)):
        writeToFiles(L,Mag,M_teq,N,Neq)
        N = float('0');
        L = float(mat[i,0])
        Neq_sav = float(mat[i,8])
        strFn = "./foutput/teqmod/" + str(int(cold)) + "_" + str(int(L)) + "_" + fName + ".dat"
        M_teq = open(strFn,"w")
        #if new value of N_eq, take mean and write to file
    elif (relTOL < (float('1.0')/(Neq_sav))*abs(mat[i,8] - Neq_sav)):
        writeToFiles(L,Mag,M_teq,N,Neq)
        N = float('0');
        Neq_sav = float(mat[i,8])
    Mag.append(mat[i,3])
    Neq.append(mat[i,8])
    Neq_sav = np.mean(Neq)
    N = N + float('1.0')
writeToFiles(L,Mag,M_teq,N,Neq)
