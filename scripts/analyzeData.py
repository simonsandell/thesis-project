import sys
import numpy as np
import math
np.set_printoptions(threshold=np.nan)

def openFiles(FileList,L,fName):
    #open files for writing
    #separate files for different systemsizes
    EF = open("./foutput/en/"+str(int(L))+"_"+fName+".dat","w")
    MF = open("./foutput/mag/"+str(int(L))+"_"+fName+".dat","w")
    BF = open("./foutput/bin/"+str(int(L))+"_"+fName+".dat","w")
    DF = open("./foutput/dbdt/"+str(int(L))+"_"+fName+".dat","w")
    XF = open("./foutput/xi/"+str(int(L))+"_"+fName+".dat","w")
    RF = open("./foutput/rs/"+str(int(L))+"_"+fName+".dat","w")
    FileList[:] = [];
    FileList.append(EF)
    FileList.append(MF)
    FileList.append(BF)
    FileList.append(DF)
    FileList.append(XF)
    FileList.append(RF)

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
    rawS2X = mat[istart:iend,14];
    rawS2Y = mat[istart:iend,15];
    rawS2Z = mat[istart:iend,16];
    #Quantities calculated for each of these averages
    rawB = mat[istart:iend,17];
    rawdBdT = mat[istart:iend,18];
    rawXI = mat[istart:iend,19];
    rawRS = mat[istart:iend,20];
    #exponential factor itself 
    rawExp= mat[istart:iend,21];
    
    #form averages from these uncorrelated MC averages
    avgrawE  = np.mean(rawE);
    avgrawE2 = np.mean(rawE2);
    avgrawM  = np.mean(rawM);
    avgrawM2 = np.mean(rawM2);
    avgrawM4 = np.mean(rawM4);
    avgrawM2E= np.mean(rawM2E);
    avgrawM4E= np.mean(rawM4E);
    avgrawS2X= np.mean(rawS2X);
    avgrawS2Y= np.mean(rawS2Y);
    avgrawS2Z= np.mean(rawS2Z);
    avgrawExp= np.mean(rawExp);

    avgE  = avgrawE/avgrawExp;
    avgE2 = avgrawE2/avgrawExp;
    avgM  = avgrawM/avgrawExp;
    avgM2 = avgrawM2/avgrawExp;
    avgM4 = avgrawM4/avgrawExp;
    avgM2E= avgrawM2E/avgrawExp;
    avgM4E= avgrawM4E/avgrawExp;
    avgS2X= avgrawS2X/avgrawExp;
    avgS2Y= avgrawS2Y/avgrawExp;
    avgS2Z= avgrawS2Z/avgrawExp;

    #calculate quantities of these averages
    calcB = avgM4/(avgM2*avgM2);
    calcdBdT = avgM4E*avgM2 + avgM4*avgM2*avgE - 2.0*avgM4*avgM2E;
    calcdBdT = (L*L*L*calcdBdT)/(T*T*avgM2*avgM2*avgM2);
    calcXI =(Nspins)*(avgM2 - avgM*avgM)/T
    calcRS = -L*avgE - L*Nspins*avgS2X/T -L*Nspins*avgS2Y/T -L*Nspins*avgS2Z/T;
    calcRS = calcRS/3.0;
    
    #Find error bars of the quantities we want to plot using jackknife method
    rawEdExp = [];
    rawMdExp = [];
    for i in range(len(rawE)):
        rawEdExp.append(rawE[i]/rawExp[i]);
        rawMdExp.append(rawM[i]/rawExp[i]);

    deltaE = jackknife(rawEdExp);
    deltaM = jackknife(rawMdExp);
    deltaB = jackknife(rawB);
    deltadBdT = jackknife(rawdBdT);
    deltaXI= jackknife(rawXI);
    deltaRS= jackknife(rawRS);

    #write T, avg, delta, N, to files
    Ylist = [avgE,avgM,calcB,calcdBdT,calcXI,calcRS];
    Deltalist = [deltaE,deltaM,deltaB,deltadBdT,deltaXI,deltaRS];


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
