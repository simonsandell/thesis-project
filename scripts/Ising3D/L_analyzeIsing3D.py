import sys
import numpy as np
import math
import jackknife
np.set_printoptions(threshold=np.nan)

def openFiles(FileList,T,fName):
    #open files for writing
    #separate files for different systemsizes
    fnfstr = "{:8.8f}"
    EF = open("./foutput/Ising3D/vsL/en/"+fnfstr.format(T)+"_"+fName+".dat","w")
    M2F = open("./foutput/Ising3D/vsL/m2/"+fnfstr.format(T)+"_"+fName+".dat","w")
    M4F = open("./foutput/Ising3D/vsL/m4/"+fnfstr.format(T)+"_"+fName+".dat","w")
    BF = open("./foutput/Ising3D/vsL/bin/"+fnfstr.format(T)+"_"+fName+".dat","w")
    XF = open("./foutput/Ising3D/vsL/xi/"+fnfstr.format(T)+"_"+fName+".dat","w")
    CF = open("./foutput/Ising3D/vsL/c/"+fnfstr.format(T)+"_"+fName+".dat","w")
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

def calcFunctions(mat):
    avgs = [];
    L = mat[0,0];
    T = mat[0,1];
    Nspins = L*L*L;
    for x in range(mat.shape[1]):
        avgs.append(np.mean(mat[:,x]));
    res = [];
    res.append(avgs[7]/avgs[18]);
    res.append(avgs[10]/avgs[18]);
    res.append(avgs[11]/avgs[18]);
    res.append(getBin(avgs[10],avgs[11],avgs[18]));
    res.append(getXI(avgs[9],avgs[10],avgs[18],T,Nspins));
    res.append(getC(avgs[7],avgs[8],avgs[18],T,Nspins));
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
    submat = mat[istart:i,:];
    functions = calcFunctions(submat);
    deltas= jackknife.getJackDelta(submat,calcFunctions,100);
    #write T, avg, delta, N, to files
    #ylist = [avge,avgm,calcb,calcdbdt,calcxi,calcrs];


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
def analyze(mat,fName):
    
    #Sort input data, by temperature, then L
    ind = np.lexsort((mat[:,18],mat[:,17],mat[:,16],mat[:,15],mat[:,14],mat[:,13],mat[:,12],mat[:,11],mat[:,10],mat[:,9],mat[:,8],mat[:,7],mat[:,5],mat[:,4],mat[:,3],mat[:,2],mat[:,6],mat[:,0],mat[:,1]));
    mat = mat[ind]
    #form averages and print to file
    L=mat[0,0];
    T=mat[0,1];
    
    FileList =[]
    openFiles(FileList,T,fName);
    
    TOL = 0.000001;
    ifirst = 0;
    for i in range(mat.shape[0]):
        #if new value of T, make new outputfile
        if(TOL < abs(mat[i,1] - T)):
            calcAvg(mat,i,ifirst,FileList);
            ifirst = i;
            L = mat[i,0]
            T = mat[i,1]
            #open new files since T has changed
            openFiles(FileList,T,fName);
        #if new L value, make new averages
        elif(TOL < abs(mat[i,0] - L)):
            calcAvg(mat,i,ifirst,FileList);
            ifirst = i;
            L = mat[i,0]
    #one final write
    calcAvg(mat,i+1,ifirst,FileList);
