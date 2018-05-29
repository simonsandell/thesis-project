import sys
import numpy as np
import math
import jackknife
np.set_printoptions(threshold=np.nan)

def openFiles(FileList,T,fName):
    #open files for writing
    #separate files for different systemsizes
    fnfstr = "{:8.8f}"
    EF = open("./foutput/3DXY/vsL/en/"+fnfstr.format(T)+"_"+fName+".dat","w")
    MF = open("./foutput/3DXY/vsL/mag/"+fnfstr.format(T)+"_"+fName+".dat","w")
    BF = open("./foutput/3DXY/vsL/bin/"+fnfstr.format(T)+"_"+fName+".dat","w")
    DF = open("./foutput/3DXY/vsL/dbdt/"+fnfstr.format(T)+"_"+fName+".dat","w")
    XF = open("./foutput/3DXY/vsL/xi/"+fnfstr.format(T)+"_"+fName+".dat","w")
    RF = open("./foutput/3DXY/vsL/rs/"+fnfstr.format(T)+"_"+fName+".dat","w")
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

def calcFunctions(mat):
    avgs = [];
    L = mat[0,0];
    T = mat[0,1];
    Nspins = L*L*L;
    for x in range(mat.shape[1]):
        avgs.append(np.mean(mat[:,x]));
    res = [];    
    res.append(abs(avgs[7])/avgs[21]);
    res.append(avgs[9]/avgs[21]);
    res.append(getBin(avgs[10],avgs[11],avgs[21]));
    res.append(getdBdT(avgs[10],avgs[11],avgs[12],avgs[13],avgs[7],avgs[21],T,Nspins));
    res.append(getXI(avgs[9],avgs[10],avgs[21],T,Nspins));
    res.append(getRS(avgs[7],avgs[14],avgs[15],avgs[16],avgs[21],L,T));
    return res;
    

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
    submat = mat[istart:iend,:];
    functions = calcFunctions(submat);
    deltas = jackknife.getJackDelta(submat,calcFunctions,100);


    fstr= "{:30.30f}";
    for i in range(len(functions)):
        FileList[i].write(fstr.format(L)+"    "+fstr.format(functions[i])+"    "+fstr.format(deltas[i])+"    "+fstr.format(N)+ "    "+fstr.format(T) + "\n")

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
    #Sort input data, by temperature, then L
    ind = np.lexsort((inData[:,21],inData[:,20],inData[:,19],inData[:,18],inData[:,17],inData[:,16],inData[:,15],inData[:,14],inData[:,13],inData[:,12],inData[:,11],inData[:,10],inData[:,9],inData[:,8],inData[:,7],inData[:,5],inData[:,4],inData[:,3],inData[:,2],inData[:,6],inData[:,0],inData[:,1]));
    sortedMat = inData[ind]

    #form averages and print to file
    L=sortedMat[0,0];
    T=sortedMat[0,1];
    
    FileList =[]
    openFiles(FileList,T,fName);
    
    TOL = 0.000001;
    ifirst = 0;
    for i in range(sortedMat.shape[0]):
        #if new value of T, make new outputfile
        if(TOL < abs(sortedMat[i,1] - T)):
            calcAvg(sortedMat,i,ifirst,FileList);
            ifirst = i;
            L = sortedMat[i,0]
            T = sortedMat[i,1]
            #open new files since T has changed
            openFiles(FileList,T,fName);
        #if new L value, make new averages
        elif(TOL < abs(sortedMat[i,0] - L)):
            calcAvg(sortedMat,i,ifirst,FileList);
            ifirst = i;
            L = sortedMat[i,0]
    #one final write
    calcAvg(sortedMat,i+1,ifirst,FileList);
