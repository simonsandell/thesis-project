import sys
import numpy as np
import math

#funcion for writing data
def writeToFiles(Mag,M_teq,N,Neq):
        meanM = np.mean(Mag);
        sqrtN = pow(N,0.5);
        deltaM = np.std(Mag)/sqrtN;
        if math.isnan(deltaM):
            deltaM = 0;
        M_teq.write(repr(Neq)+"    "+repr(meanM)+"    "+repr(deltaM)+"\n")
        Mag[:]= []
        N = 0.0
        
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
ind = np.lexsort((mat[:,8],mat[:,6],mat[:,5],mat[:,4],mat[:,3],mat[:,2],mat[:,1],mat[:,7],mat[:,0]))
mat = mat[ind]

L=mat[0,0];
Neq = mat[0,7];
Mag=[];
N = 0.0;

#open files for writing

M_teq = open("./foutput/teq/"+str(int(L))+"_"+fName+".dat","w")

TOL = 10e-10
for i in range(mat.shape[0]):
    #if new value of L, make new outputfile
    if(TOL < abs(mat[i,0] - L)):
        writeToFiles(Mag,M_teq,N,Neq)
        L = float(mat[i,0])
        Neq = float(mat[i,7])
        M_teq = open("./foutput/teq/"+str(int(L))+"_"+fName+".dat","w")
    elif (TOL < abs(mat[i,7] - Neq)):
        writeToFiles(Mag,M_teq,N,Neq)
        Neq = float(mat[i,7])
    Mag.append(mat[i,3])
    N = N + 1.0   
writeToFiles(Mag,M_teq,N,Neq)
