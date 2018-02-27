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
    newBF = open("./foutput/bin/"+str(int(L))+"_"+fName+"new.dat","w")
    XF = open("./foutput/xi/"+str(int(L))+"_"+fName+".dat","w")
    newXF = open("./foutput/xi/"+str(int(L))+"_"+fName+"new.dat","w")
    CF= open("./foutput/c/"+str(int(L))+"_"+fName+".dat","w")
    newCF = open("./foutput/c/"+str(int(L))+"_"+fName+"new.dat","w")

    FileList[:] = [];
    FileList.append(EF)
    FileList.append(M2F)
    FileList.append(M4F)
    FileList.append(BF)
    FileList.append(newBF)
    FileList.append(XF)
    FileList.append(newXF)
    FileList.append(CF)
    FileList.append(newCF)

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
# 14     15     16     17     18     
# bin    dBdT   xi     c      expFac
# incoming values are per spin and not divided by avgExpFac
# except for bin,dbdt,xi and c which should be ready to write to file    
    B = np.mean(mat[istart:iend,14]);
    xi = np.mean(mat[istart:iend,16]);
    c = np.mean(mat[istart:iend,17]);

    expFac = np.mean(mat[istart:iend,18]);
    
    Elist = mat[istart:iend,7];
    Elist[:] = [x/expFac for x in Elist];
    E = np.mean(Elist);
    
    E2list = mat[istart:iend,8];
    E2list[:] = [x/expFac for x in E2list];
    E2 = np.mean(E2list);
    calcB = expFac*M4/pow(M2,2);

    Mlist = mat[istart:iend,9];
    Mlist[:] = [x/expFac for x in Mlist];
    M = np.mean(Mlist);
    
    M2list = mat[istart:iend,10];
    M2list[:] = [x/expFac for x in M2list];
    M2 = np.mean(M2list);

    M4list = mat[istart:iend,11];
    M4list[:] = [x/expFac for x in M4list];
    M4 = np.mean(M4list);

    M2Elist = mat[istart:iend,12];
    M2Elist[:] = [x/expFac for x in M2Elist];
    M2E = np.mean(M2list);

    M4Elist = mat[istart:iend,13];
    M4Elist[:] = [x/expFac for x in M4Elist];
    M4E = np.mean(M4Elist);

    calcxi = (M2 ) - M*M/(expFac*expFac);
    calcxi = calcxi*(L*L*L)/T;

    calcC = (E2/expFac - Eps);
    calcC = calcC*(L*L*L*L*L*L);
    calcC = calcC/(T*T);

    Ylist = [Eps,M2,M4,B,calcB,xi,calcxi,c,calcC];


    deltaexpFac = np.std(mat[istart:iend,18])/pow(N,0.5);
    deltaE = np.std(Elist)/pow(N,0.5);
    deltaE2 = np.std(mat[istart:iend,8])/pow(N,0.5);
    deltaM2 = np.std(mat[istart:iend,10])/pow(N,0.5);
    deltaM4 = np.std(mat[istart:iend,11])/pow(N,0.5);
    deltaM2E = np.std(mat[istart:iend,12])/pow(N,0.5);
    deltaM4E = np.std(mat[istart:iend,13])/pow(N,0.5);
    deltaB = np.std(mat[istart:iend,14])/pow(N,0.5);
    deltaxi = np.std(mat[istart:iend,16])/pow(N,0.5);
    deltaC = np.std(mat[istart:iend,17])/pow(N,0.5);
    Deltalist = [deltaE,deltaM2,deltaM4,deltaB,0,deltaxi,0,deltaC,0];
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
