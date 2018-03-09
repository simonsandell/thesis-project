import sys
import numpy as np
import math
np.set_printoptions(threshold=np.nan)

def openFiles():
    o1file = open("./foutput/3DXY/omega/omega1.dat","w")
    o2file = open("./foutput/3DXY/omega/omega2.dat","w")
    o3file = open("./foutput/3DXY/omega/omega3.dat","w")
    o4file = open("./foutput/3DXY/omega/omega4.dat","w")
    r1file = open("./foutput/3DXY/rs_corr/rscorr1.dat","w")
    r2file = open("./foutput/3DXY/rs_corr/rscorr2.dat","w")
    r3file = open("./foutput/3DXY/rs_corr/rscorr3.dat","w")
    r4file = open("./foutput/3DXY/rs_corr/rscorr4.dat","w")
    return [o1file,o2file,o3file,o4file,r1file,r2file,r3file,r4file];
def calcCorrections(avgs):
    bdiff = avgs[1][2] - avgs[0][2];
    bdiff2 = avgs[2][2] - avgs[1][2];
    bdiv = bdiff2/bdiff
    omega = -math.log(bdiv)/math.log(2)

    rdiff = avgs[1][1] - avgs[0][1];
    rdiff2 = avgs[2][1] - avgs[1][1];
    rdiv = rdiff2/rdiff;
    #rscorr = -math.log(rdiv)/math.log(2);
    return [1.0,omega]

def calcAvgs(mat):
    L = mat[0,0];
    T = mat[0,1];
    M2 = np.mean(mat[:,10]);
    M4 = np.mean(mat[:,11]);
    Exp = np.mean(mat[:,21]);
    b = Exp*M4/(M2*M2);
    E = np.mean(mat[:,7]);
    S2X = np.mean(mat[:,14]);
    S2Y = np.mean(mat[:,15]);
    S2Z = np.mean(mat[:,16]);
    rs = -L*E - (L*L*L*L/T)*(S2X + S2Y + S2Z);
    rs = rs/(3.0*Exp);
    return [L,rs,b]

def analyze(mat,i,istart,FileList):
# Format::
# 0      1      2      3      4      5      6            
# L      T      neqsw  neqcl  nsmsw  nsmcl  cold
#
# 7      8      9      10     11     12     13                
# E      E2     M      M2     M4     M2E    M4E
#
# 14     15     16     17     18     19     20     21                
# S2X    S2Y    S2Z    bin    dBdT   xi     rs     expFac
    iend = i -1;
    submat = mat[istart:iend,:];
    T = submat[0,1];
    submatL = submat[:,0];
    L_list = np.unique(submatL);
    N_L = L_list.shape[0];
    j = 0;
    avgs = []
    for l in L_list:
        #find start and end index for each L
        foundstart = False;
        foundend = False;
        lstart = 0;
        lend = 0;
        for j in range(submat.shape[0]):
            if (submat[j,0] == l) and (not foundstart):
                lstart = j;
                foundstart= True
            if (submat[j,0] != l) and foundstart and (not foundend):
                lend = j;
                foundend= True;
        if (not foundend):
            lend = j;
        subL = submat[lstart:lend,:];
        print(lstart);
        print(lend);

        avgs.append(calcAvgs(subL));

    fstr= "{:30.30f}";
    for k in range(N_L-2):
        corrs = calcCorrections(avgs[k:k+3]);
        print(corrs)
        #FileList[k].write(fstr.format(T) + "    " + fstr.format(corrs[1]) + "    " + 
                #fstr.format(0.0) + " \n"); 
        #FileList[k+4].write(fstr.format(T) + "    " + fstr.format(corrs[0]) + "    " + 
                #fstr.format(0.0) + " \n"); 
        FileList[k].write(repr(T) + "    " + repr(corrs[1]) + "    " + 
                repr(0.0) + " \n"); 
        FileList[k+4].write(repr(T) + "    " + repr(corrs[0]) + "    " + 
                repr(0.0) + " \n"); 




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
fName= sys.argv[1];
data0 = open("./output/3DXY/" + fName,"r")
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
T = mat[0,1];

TOL = 0.000001;
ifirst = 0;
filelist = openFiles();
for i in range(mat.shape[0]):
    if (mat[i,1] != T):
        analyze(mat,i,ifirst,filelist);
        ifirst = i;
        T = mat[i,1];
        
#one final write
analyze(mat,i+1,ifirst,filelist);
