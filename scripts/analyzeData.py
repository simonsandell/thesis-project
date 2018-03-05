import sys
import numpy as np
import math

def openFiles(FileList,L,fName):
    #open files for writing
    #separate files for different systemsizes
    EF = open("./foutput/en/"+str(int(L))+"_"+fName+".dat","w")
    M2F = open("./foutput/m2/"+str(int(L))+"_"+fName+".dat","w")
    M4F = open("./foutput/m4/"+str(int(L))+"_"+fName+".dat","w")
    BF = open("./foutput/bin/"+str(int(L))+"_"+fName+".dat","w")
    XF = open("./foutput/xi/"+str(int(L))+"_"+fName+".dat","w")
    CF= open("./foutput/c/"+str(int(L))+"_"+fName+".dat","w")

    FileList[:] = [];
    FileList.append(EF)
    FileList.append(M2F)
    FileList.append(M4F)
    FileList.append(BF)
    FileList.append(XF)
    FileList.append(CF)


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
# 14     15     16     17     18     
# bin    dBdT   xi     c      expFac
# incoming values are per spin and not divided by avgExpFac
# except for bin,dbdt,xi and c which are calculated from each set of averages and should be used in jackknife only
    N = i - istart;
    T = mat[istart,1];
    L = mat[istart,0];
    iend = i -1;
    Nspins = L*L*L;

    #MC averages not divided by exponential factor
    rawE = mat[istart:iend,7];
    rawE2 = mat[istart:iend,8];
    rawM = mat[istart:iend,9];
    rawM2 = mat[istart:iend,10];
    rawM4 = mat[istart:iend,11];
    rawM2E = mat[istart:iend,12];
    rawM4E = mat[istart:iend,13];
    #Quantities calculated for each of these averages
    rawB = mat[istart:iend,14];
    rawdBdT = mat[istart:iend,15];
    rawXI = mat[istart:iend,16];
    rawC = mat[istart:iend,17];
    #exponential factor itself 
    rawExp= mat[istart:iend,18];
    
    #form averages from these uncorrelated MC averages
    avgrawE  = np.mean(rawE);
    avgrawE2 = np.mean(rawE2);
    avgrawM  = np.mean(rawM);
    avgrawM2 = np.mean(rawM2);
    avgrawM4 = np.mean(rawM4);
    avgrawM2E= np.mean(rawM2E);
    avgrawM4E= np.mean(rawM4E);
    avgrawExp= np.mean(rawExp);

    avgE  = avgrawE/avgrawExp;
    avgE2 = avgrawE2/avgrawExp;
    avgM  = avgrawM/avgrawExp;
    avgM2 = avgrawM2/avgrawExp;
    avgM4 = avgrawM4/avgrawExp;
    avgM2E= avgrawM2E/avgrawExp;
    avgM4E= avgrawM4E/avgrawExp;

    #calculate quantities of these averages
    calcB = avgM4/(avgM2*avgM2);
    calcdBdT = avgM4E*avgM2 + avgM4*avgM2*avgE - 2.0*avgM4*avgM2E;
    calcdBdT = (L*L*L*calcdBdT)/(T*T*avgM2*avgM2*avgM2);
    calcXI = avgM2 - (avgM*avgM);
    calcXI = calcXI/T;
    calcXI = calcXI*Nspins;
    calcC = avgE2 - avgE*avgE;
    calcC = calcC/(T*T);
    calcC = Nspins*Nspins*calcC;
    
    #Find error bars of the quantities we want to plot using jackknife method
    rawEdExp = [];
    rawM2dExp = [];
    rawM4dExp = [];
    for i in range(len(rawE)):
        rawEdExp.append(rawE[i]/rawExp[i]);
        rawM2dExp.append(rawM2[i]/rawExp[i]);
        rawM4dExp.append(rawM4[i]/rawExp[i]);

    deltaE = jackknife(rawEdExp);
    deltaM2 = jackknife(rawM2dExp);
    deltaM4 = jackknife(rawM4dExp);
    deltaB = jackknife(rawB);
    deltadBdT = jackknife(rawdBdT);
    deltaXI= jackknife(rawXI);
    deltaC= jackknife(rawC);

    Ylist = [avgE,avgM2,avgM4,calcB,calcXI,calcC];
    Deltalist = [deltaE,deltaM2,deltaM4,deltaB,deltaXI,deltaC];

    for i in range(len(Ylist)):
        FileList[i].write(repr(T)+"    "+repr(Ylist[i])+"    "+repr(Deltalist[i])+"    "+repr(N)+"\n")


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
# 14     15     16     17     18    
# bin    dBdT   xi     c      expFac
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
ind = np.lexsort((mat[:,18],mat[:,17],mat[:,16],mat[:,15],mat[:,14],mat[:,13],mat[:,12],mat[:,11],mat[:,10],mat[:,9],mat[:,8],mat[:,7],mat[:,5],mat[:,4],mat[:,3],mat[:,2],mat[:,6],mat[:,1],mat[:,0]));
mat = mat[ind]

#form averages and print to file
L=mat[0,0];
T=mat[0,1];

FileList =[]
openFiles(FileList,L,fName);

TOL = float('0.00000000001');
ifirst = 0;
for i in range(mat.shape[0]):
    #if new value of L, make new outputfile
    if(TOL < abs(mat[i,0] - L)):
        calcAvg(mat,i,ifirst,FileList);
        ifirst = i;
        L = float(mat[i,0])
        T = float(mat[i,1])
        #open new files since L has changed
        openFiles(FileList,L,fName);
    elif(TOL < abs(mat[i,1] - T)):
        calcAvg(mat,i,ifirst,FileList);
        ifirst = i;
        T = float(mat[i,1])
#one final write
calcAvg(mat,i+1,ifirst,FileList);
