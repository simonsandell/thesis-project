import sys
import numpy as np
import math
np.set_printoptions(threshold=np.nan)

def openFiles(FileList,N,fName):
    o1file = open("./foutput/omega/omega1.dat","a")
    o2file = open("./foutput/omega/omega2.dat","a")
    o3file = open("./foutput/omega/omega3.dat","a")
    o4file = open("./foutput/omega/omega4.dat","a")
    r1file = open("./foutput/rs_corr/rscorr1.dat","a")
    r2file = open("./foutput/rs_corr/rscorr2.dat","a")
    r3file = open("./foutput/rs_corr/rscorr3.dat","a")
    r4file = open("./foutput/rs_corr/rscorr4.dat","a")
    FileList= [o1file,o2file,o3file,o4file,r1file,r2file,r3file,r4file];
def closeFiles(FileList):
    for f in FileList:
        f.close();

def jackknife(flist):
    jacklen = float(len(flist))-1.0;
    listsum = sum(flist);
    jacklist = [];
    
    for i in range(len(flist)):
        jacklist.append(listsum);
        jacklist[i] = jacklist[i] - flist[i];
        jacklist[i] = jacklist[i]/(jacklen);
    jackavg = np.mean(jacklist);
    sigmaf = pow(jacklen,0.5)*(np.std(jacklist));
    return sigmaf;
    

def calcAvg(mat,i,istart,FileList):
# Format::
# 0      1      2      3      4      5      6            
# L      T      neqsw  neqcl  nsmsw  nsmcl  cold
#
# 7      8      9      10     11     12     13                
# E      E2     M      M2     M4     M2E    M4E
#
# 14     15     16     17     18     19     20     21                
# S2X    S2Y    S2Z    bin    dBdT   xi     rs     expFac

    T = mat[istart,1];
    startL = mat[istart,0];
    N_L = 1;
    avgB = []
    starti = istart;
    endi = 0;
    for x in range(i-istart):
        if (mat[x,0] != startL):
            endi = x-1;
            N_L = N_L +1;
            startL = mat[x,0];
            avgExp= np.mean(mat[starti:endi,21]);
            avgM2= np.mean(mat[starti:endi,10]);
            avgM4= np.mean(mat[starti:endi,11]);
            avgB.append((avgExp*avgM4/(avgM2*avgM2)));
            rawB.append(mat[starti:endi,17]);
            starti = x;
    for y in range(N_L -2):
        
    fstr= "{:30.30f}";
    for i in range(len(Ylist)):
        FileList[i].write(fstr.format(L)+"    "+fstr.format(Ylist[i])+"    "+fstr.format(Deltalist[i])+"    "+fstr.format(N)+ "    "+fstr.format(T) + "\n")

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

#Sort input data, by temperature, then L
ind = np.lexsort((mat[:,21],mat[:,20],mat[:,19],mat[:,18],mat[:,17],mat[:,16],mat[:,15],mat[:,14],mat[:,13],mat[:,12],mat[:,11],mat[:,10],mat[:,9],mat[:,8],mat[:,7],mat[:,5],mat[:,4],mat[:,3],mat[:,2],mat[:,6],mat[:,0],mat[:,1]));
mat = mat[ind]
#form averages and print to file
startL=mat[0,0];
currL=mat[0,0];


TOL = 0.000001;
ifirst = 0;
for i in range(mat.shape[0]):
    if (mat[i,0] == startL) and (mat[i,0] != currL):
        calcAvg(mat,i,ifirst);
        ifirst = i;
    currL = mat[i,0];
        
#one final write
calcAvg(mat,i+1,ifirst);
