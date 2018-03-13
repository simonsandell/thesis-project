import sys
import numpy as np
import math
import jackknife
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
# 14     15     16     17     18    
# bin    dBdT   xi     c      expFac

    N = i - istart;
    iend = i -1;

    L = mat[istart,0];
    T = mat[istart,1];
    Nspins = L*L*L;
    #MC averages not divided by exponential factor
    submat = mat[istart:i,:];
    functions = calcFunctions(submat);
    deltas = jackknife.getJackDelta(submat,calcFunctions,100);

    fstr= "{:30.30f}";
    for i in range(len(functions)):
        FileList[i].write(fstr.format(T)+"    "+fstr.format(functions[i])+"    "+fstr.format(deltas[i])+"    "+fstr.format(N)+"\n")

#
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
def analyze(inData,fName):
    
    #Sort input data    
    ind = np.lexsort((inData[:,18],inData[:,17],inData[:,16],inData[:,15],inData[:,14],inData[:,13],inData[:,12],inData[:,11],inData[:,10],inData[:,9],inData[:,8],inData[:,7],inData[:,5],inData[:,4],inData[:,3],inData[:,2],inData[:,6],inData[:,1],inData[:,0]));
    mat = inData[ind]
    
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
