import sys
import numpy as np
import math
np.set_printoptions(threshold=np.nan)

def openFiles(FileList,L,fName):
    #open files for writing
    #separate files for different systemsizes
    EF = open("./foutput/Ising3D/en/"+str(int(L))+"_"+fName+".dat","w")
    M2F = open("./foutput/Ising3D/m2/"+str(int(L))+"_"+fName+".dat","w")
    M4F = open("./foutput/Ising3D/m4/"+str(int(L))+"_"+fName+".dat","w")
    BF = open("./foutput/Ising3D/bin/"+str(int(L))+"_"+fName+".dat","w")
    CF = open("./foutput/Ising3D/c/"+str(int(L))+"_"+fName+".dat","w")
    XF = open("./foutput/Ising3D/xi/"+str(int(L))+"_"+fName+".dat","w")
    FileList[:] = [];
    FileList.append(EF)
    FileList.append(M2F)
    FileList.append(M4F)
    FileList.append(BF)
    FileList.append(XF)
    FileList.append(CF)

def getBin(m2,m4,exp):
    return (m4*exp)/(m2*m2);

def getXI(m,m2,exp,T,Nspins):
    return Nspins*(m2/exp - m*m/(exp*exp))/T

def getC(e,e2,exp,T,Nspins):
    c = e2/exp - e*e/(exp*exp);
    c = c/(T*T);
    c = c*Nspins*Nspins;
    return c;

def jackAvg(qlist):
    javg = [];
    for i in range(qlist.shape[0]):
        javg.append(np.mean(np.concatenate((qlist[:i],qlist[i+1:]))));
    return javg;

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

    N = i - istart;
    iend = i -1;

    L = mat[istart,0];
    T = mat[istart,1];
    Nspins = L*L*L;
    #MC averages not divided by exponential factor
    rawE = mat[istart:iend,7];
    rawE2 = mat[istart:iend,8];
    rawM = mat[istart:iend,9];
    rawM2 = mat[istart:iend,10];
    rawM4 = mat[istart:iend,11];
    rawM2E = mat[istart:iend,12];
    rawM4E = mat[istart:iend,13];
    #Quantities calculated for each of these averages, doesnt really need these
    rawB = mat[istart:iend,14];
    rawdBdT = mat[istart:iend,15];
    rawXI = mat[istart:iend,16];
    rawC = mat[istart:iend,17];
    #exponential factor 
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
    calcdBdT = (Nspins*calcdBdT)/(T*T*avgM2*avgM2*avgM2);
    calcXI =(Nspins)*(avgM2 - avgM*avgM)/T
    calcC = avgE2 - avgE*avgE;
    calcC = calcC/(T*T);
    calcC = Nspins*Nspins*calcC;

    #Find error bars of the quantities we want to plot using jackknife method
    javgExp= jackAvg(rawExp);
    javgE  = jackAvg(rawE); 
    javgE2 = jackAvg(rawE2);
    javgM  = jackAvg(rawM); 
    javgM2 = jackAvg(rawM2);
    javgM4 = jackAvg(rawM4);
    javgM2E= jackAvg(rawM2E);
    javgM4E= jackAvg(rawM4E);
    jE = [];
    jM2 = [];
    jM4 = [];
    jB = [];
    jX = [];
    jC = [];
    for i in range(len(javgE)):
        jE.append(javgE[i]/javgExp[i]);
        jM2.append(javgM2[i]/javgExp[i]);
        jM4.append(javgM4[i]/javgExp[i]);
        jB.append(getBin(javgM2[i],javgM4[i],javgExp[i]));
        jX.append(getXI(javgM[i],javgM2[i],javgExp[i],T,Nspins));
        jC.append(getC(javgE[i],javgE2[i],javgExp[i],T,Nspins));

    jList = [jE,jM2,jM4,jB,jX,jC]
    Deltalist = [];
    Deltalist[:] = []
    for l in jList:
        Deltalist.append(pow(len(l),0.5)*np.std(l));

    #write T, avg, delta, N, to files
    Ylist = [avgE,avgM2,avgM4,calcB,calcXI,calcC];


    fstr= "{:30.30f}";
    for i in range(len(Ylist)):
        FileList[i].write(fstr.format(T)+"    "+fstr.format(Ylist[i])+"    "+fstr.format(Deltalist[i])+"    "+fstr.format(N)+"\n")

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
data0 = open("./output/Ising3D/" + fName,"r")
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
