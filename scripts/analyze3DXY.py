import numpy as np
import math
np.set_printoptions(threshold=np.nan)

def openFiles(FileList,L,fName):
    #open files for writing
    #separate files for different systemsizes
    EF = open("./foutput/3DXY/en/"+str(int(L))+"_"+fName+".dat","w")
    MF = open("./foutput/3DXY/mag/"+str(int(L))+"_"+fName+".dat","w")
    BF = open("./foutput/3DXY/bin/"+str(int(L))+"_"+fName+".dat","w")
    DF = open("./foutput/3DXY/dbdt/"+str(int(L))+"_"+fName+".dat","w")
    XF = open("./foutput/3DXY/xi/"+str(int(L))+"_"+fName+".dat","w")
    RF = open("./foutput/3DXY/rs/"+str(int(L))+"_"+fName+".dat","w")
    FileList[:] = [];
    FileList.append(EF)
    FileList.append(MF)
    FileList.append(BF)
    FileList.append(DF)
    FileList.append(XF)
    FileList.append(RF)


def getBin(m2,m4,exp):
    return (m4*exp)/(m2*m2);

def getdBdT(M2,M4,M2E,M4E,E,Exp,T,Nspins):
    dbdt= Exp*M4E*M2 + M4*M2*E - 2.0*M4*M2E*Exp;
    dbdt= Nspins*dbdt/(T*T*M2*M2*M2);
    return dbdt;
def getXI(m,m2,exp,T,Nspins):
    return Nspins*(m2/exp - m*m/(exp*exp))/T
def getRS(e,sx,sy,sz,exp,L,T):
    rs = -L*e -(L*L*L*L/T)*(sx +sy +sz);
    rs = rs/(3.0*exp);
    return rs;


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
    calcdBdT = (Nspins*calcdBdT)/(T*T*avgM2*avgM2*avgM2);
    calcXI =(Nspins)*(avgM2 - avgM*avgM)/T
    calcRS = -L*avgE - L*Nspins*avgS2X/T -L*Nspins*avgS2Y/T -L*Nspins*avgS2Z/T;
    calcRS = calcRS/3.0;
    
    #Find error bars of the quantities we want to plot using jackknife method
    javgExp= jackAvg(rawExp);
    javgE  = jackAvg(rawE); 
    javgE2 = jackAvg(rawE2);
    javgM  = jackAvg(rawM); 
    javgM2 = jackAvg(rawM2);
    javgM4 = jackAvg(rawM4);
    javgM2E= jackAvg(rawM2E);
    javgM4E= jackAvg(rawM4E);
    javgS2X= jackAvg(rawS2X);
    javgS2Y= jackAvg(rawS2Y);
    javgS2Z= jackAvg(rawS2Z);
    jE = [];
    jM = [];
    jB = [];
    jD = [];
    jX = [];
    jR = [];
    for i in range(len(javgE)):
        jE.append(javgE[i]/javgExp[i]);
        jM.append(javgM[i]/javgExp[i]);
        jB.append(getBin(javgM2[i],javgM4[i],javgExp[i]));
        jD.append(getdBdT(javgM2[i],javgM4[i],javgM2E[i],javgM4E[i],javgE[i],javgExp[i],T,Nspins));
        jX.append(getXI(javgM[i],javgM2[i],javgExp[i],T,Nspins));
        jR.append(getRS(javgE[i],javgS2X[i],javgS2Y[i],javgS2Z[i],javgExp[i],L,T));

    jList = [jE,jM,jB,jD,jX,jR]
    Deltalist = [];
    Deltalist[:] = []
    for l in jList:
        Deltalist.append(pow(len(l),0.5)*np.std(l));

    #write T, avg, delta, N, to files
    Ylist = [avgE,avgM,calcB,calcdBdT,calcXI,calcRS];


    #fstr= "{:30.30f}";
    for i in range(len(Ylist)):
        #FileList[i].write(fstr.format(T)+"    "+fstr.format(Ylist[i])+"    "+fstr.format(Deltalist[i])+"    "+fstr.format(N)+"\n")
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
# 14     15     16     17     18     19     20     21                
# SX     SY     SZ     bin    dBdT   xi     rs     expFac
def analyze(inData,fName):

    #Sort input data    
    print(inData.shape);
    inData = np.squeeze(inData);
    print(inData.shape);
    ind = np.lexsort((inData[:,21],inData[:,20],inData[:,19],inData[:,18],inData[:,17],inData[:,16],inData[:,15],inData[:,14],inData[:,13],inData[:,12],inData[:,11],inData[:,10],inData[:,9],inData[:,8],inData[:,7],inData[:,5],inData[:,4],inData[:,3],inData[:,2],inData[:,6],inData[:,1],inData[:,0]));
    sortedMat= inData[ind];
    sortedMat = np.squeeze(sortedMat);
    
    #form averages and print to file
    L=sortedMat[0,0];
    T=sortedMat[0,1];
    
    FileList =[]
    openFiles(FileList,L,fName);
    
    TOL = float('0.00000000001');
    ifirst = 0;
    for i in range(sortedMat.shape[0]):
        #if new value of L, make new outputfile
        if(TOL < abs(sortedMat[i,0] - L)):
            calcAvg(sortedMat,i,ifirst,FileList);
            ifirst = i;
            L = float(sortedMat[i,0])
            T = float(sortedMat[i,1])
            #open new files since L has changed
            openFiles(FileList,L,fName);
        elif(TOL < abs(sortedMat[i,1] - T)):
            calcAvg(sortedMat,i,ifirst,FileList);
            ifirst = i;
            T = float(sortedMat[i,1])
    #one final write
    calcAvg(sortedMat,i+1,ifirst,FileList);
