import sys
import numpy as np
import math

#funcion for writing data
def writeToFiles(Mag,M_teq,N,Neq):
        meanNeq = np.mean(Neq);
        meanM = np.mean(Mag);
        sqrtN = pow(N,0.5);
        deltaM = np.std(Mag)/sqrtN;
        if math.isnan(deltaM):
            deltaM = 0;
        M_teq.write(repr(meanNeq)+"    "+repr(meanM)+"    "+repr(deltaM)+"\n")
        Mag[:]= []
        Neq[:]= []
        
arguments = sys.argv
fName = arguments[1]
data0 = open("./output/" + fName,"r")
vals = []
for ln in data0:
    strlist = ln.rsplit(" ")
    strlist = [x for x in strlist if not (x=="\n")]
    fllist = [float(x) for x in strlist] 
    vals.append(fllist)

#sort by L, N_equil, T 
mat = np.array(vals)
ind = np.lexsort((mat[:,7],mat[:,6],mat[:,5],mat[:,4],mat[:,3],mat[:,2],mat[:,1],mat[:,9],mat[:,8],mat[:,10],mat[:,0]))
mat = mat[ind]

cold = float(mat[0,10])
L=float(mat[0,0])
Neq_sav = float(mat[0,8])
Neq = [];
Mag=[];
N = 0.0;

#open files for writing
strFn = "./foutput/teq/" + str(int(cold)) + "_" + str(int(L)) + "_" + fName + ".dat"
M_teq = open(strFn,"w")

TOL = 5 
for i in range(mat.shape[0]):
    #if new value of L or cold, make new outputfile
    if (abs(mat[i,10] - cold) >0.1):
        writeToFiles(Mag,M_teq,N,Neq)
        N = 0;
        L=float(mat[i,0])
        Neq_sav = float(mat[i,8])
        cold = float(mat[i,10])
        strFn = "./foutput/teq/" + str(int(cold)) + "_" + str(int(L)) + "_" + fName + ".dat"
        M_teq = open(strFn,"w")
    elif(TOL < abs(mat[i,0] - L)):
        writeToFiles(Mag,M_teq,N,Neq)
        N = 0;
        L = float(mat[i,0])
        Neq_sav = float(mat[i,8])
        strFn = "./foutput/teq/" + str(int(cold)) + "_" + str(int(L)) + "_" + fName + ".dat"
        M_teq = open(strFn,"w")
        #if new value of N_eq, take mean and write to file
    elif (TOL < abs(mat[i,8] - Neq_sav)):
        writeToFiles(Mag,M_teq,N,Neq)
        N = 0;
        Neq_sav = float(mat[i,8])
    Mag.append(mat[i,3])
    Neq.append(mat[i,8])
    N = N + 1.0   
writeToFiles(Mag,M_teq,N,Neq)
