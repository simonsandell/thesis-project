import sys
import numpy as np
import math

def openFiles(FileList,L,fName):
    #open files for writing
    #separate files for different systemsizes
    EF = open("./foutput/en/"+str(int(L))+"_"+fName+".dat","w")
    MF = open("./foutput/mag/"+str(int(L))+"_"+fName+".dat","w")
    BF = open("./foutput/bin/"+str(int(L))+"_"+fName+".dat","w")
    newBF = open("./foutput/bin/"+str(int(L))+"_"+fName+"new.dat","w")
    DF = open("./foutput/dbdt/"+str(int(L))+"_"+fName+".dat","w")
    newDF = open("./foutput/dbdt/"+str(int(L))+"_"+fName+"new.dat","w")
    XF = open("./foutput/xi/"+str(int(L))+"_"+fName+".dat","w")
    newXF = open("./foutput/xi/"+str(int(L))+"_"+fName+"new.dat","w")
    RF = open("./foutput/rs/"+str(int(L))+"_"+fName+".dat","w")
    newRF = open("./foutput/rs/"+str(int(L))+"_"+fName+"new.dat","w")
    FileList[:] = [];
    FileList.append(EF)
    FileList.append(MF)
    FileList.append(BF)
    FileList.append(newBF)
    FileList.append(DF)
    FileList.append(newDF)
    FileList.append(XF)
    FileList.append(newXF)
    FileList.append(RF)
    FileList.append(newRF)
    

def calcAvg(mat,i,istart,FileList):
    N = i - istart;
    T = mat[istart,1];
    L = mat[istart,0];
    iend = i -1;
# Format::
# 0      1      2      3      4      5      6            
# L      T      neqsw  neqcl  nsmsw  nsmcl  cold
#
# 7      8      9      10     11     12     13                
# E      E2     M      M2     M4     M2E    M4E
#
# 14     15     16     17     18     19     20     21                
# SX     SY     SZ     bin    dBdT   xi     rs     expFac
# incoming values are per spin and not divided by avgExpFac
    expFac = np.mean(mat[istart:iend,21]);
    E = np.mean(mat[istart:iend,7]);
    Elist = mat[istart:iend,7];
    Elist[:] = [x /expFac for x in Elist];
    Eps = np.mean(Elist);
    E2 = np.mean(mat[istart:iend,8]);
    M = np.mean(mat[istart:iend,9]);
    Mlist = mat[istart:iend,9];
    Mlist[:] = [x /expFac for x in Mlist];
    Mps = np.mean(Mlist);
    M2 = np.mean(mat[istart:iend,10]);
    M4 = np.mean(mat[istart:iend,11]);
    M2E = np.mean(mat[istart:iend,12]);
    M4E = np.mean(mat[istart:iend,13]);
    SX = np.mean(mat[istart:iend,14]);
    SY = np.mean(mat[istart:iend,15]);
    SZ = np.mean(mat[istart:iend,16]);
    B = np.mean(mat[istart:iend,17]);
    dBdT = np.mean(mat[istart:iend,18]);
    xi = np.mean(mat[istart:iend,19]);
    rs = np.mean(mat[istart:iend,20]);
    

    calcB = expFac*M4/pow(M2,2);
    calcdBdT =  expFac*M4E*M2 + M4*M2*E -2.0*expFac*M4*M2E;
    calcdBdT = calcdBdT*L*L*L;
    calcdBdT = calcdBdT/(T*T*M2*M2*M2);
    calcxi = (M2/ expFac) - M*M/(expFac*expFac);
    calcxi = calcxi*(L*L*L)/T;
    calcrs = -E -SX/T - SY/T - SZ/T;
    calcrs = calcrs*L/(3.0*expFac);

    Ylist = [Eps,Mps,B,calcB,dBdT,calcdBdT,xi,calcxi,rs,calcrs];


    deltaexpFac = np.std(mat[istart:iend,21])/pow(N,0.5);
    deltaE = np.std(Elist)/pow(N,0.5);
    deltaE2 = np.std(mat[istart:iend,8])/pow(N,0.5);
    deltaM = np.std(Mlist)/pow(N,0.5);
    deltaM2 = np.std(mat[istart:iend,10])/pow(N,0.5);
    deltaM4 = np.std(mat[istart:iend,11])/pow(N,0.5);
    deltaM2E = np.std(mat[istart:iend,12])/pow(N,0.5);
    deltaM4E = np.std(mat[istart:iend,13])/pow(N,0.5);
    deltaSX = np.std(mat[istart:iend,14])/pow(N,0.5);
    deltaSY = np.std(mat[istart:iend,15])/pow(N,0.5);
    deltaSZ = np.std(mat[istart:iend,16])/pow(N,0.5);
    deltaB = np.std(mat[istart:iend,17])/pow(N,0.5);
    deltadBdT = np.std(mat[istart:iend,18])/pow(N,0.5);
    deltaxi = np.std(mat[istart:iend,19])/pow(N,0.5);
    deltars = np.std(mat[istart:iend,20])/pow(N,0.5);
    Deltalist = [deltaE,deltaM,deltaB,0,deltadBdT,0,deltaxi,0,deltars,0];
    for i in range(len(Ylist)):
        FileList[i].write(repr(T)+"    "+repr(Ylist[i])+"    "+repr(Deltalist[i])+"    "+repr(N)+"\n")
        #FileList[i].write(repr(T)+"    "+repr(Ylist[i])+"    "+repr(0.0)+"    "+repr(N)+"\n")

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
