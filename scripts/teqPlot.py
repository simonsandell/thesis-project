import jackknife

import numpy as np

#returns avg mag
def jfunc(mat):
    return np.mean(mat[:,9]);

def writeLine(mat,openfile):
    avgM = jfunc(mat);
    delM = jackknife.getJackDelta(mat,jfunc,100);
    fstr= "{:30.30f}";
    openfile.write(fstr.format(mat[0,4]) + "    " + fstr.format(avgM) + "    " + fstr.format(delM) + str(mat.shape[0]));


def oneTemp(mat,openfile):
    startI = 0;
    curr_N= mat[0,4];
    for i in range(mat.shape[0]):
        if (curr_N != mat[i,4]):
            writeLine(mat[startI:i],openfile);
            curr_N = mat[i,4];
            startI = i;
    writeLine(mat[startI:,:],openfile);

    

def oneSize(mat,temp,openfile):
    for i in range(mat.shape[0]):
        if (abs(mat[i,1] - temp) > TOL):
            i = i+1;
        else:
            startI = i;
            while True:
                if (abs(mat[i,1] - temp)< TOL):
                    i = i +1;
                else:
                    break;

            break;
    oneTemp(mat[startI:i,:],openfile);

#sort by L, then NTotSweeps
def analyze(mat,folderpath,temp):
    ind = np.lexsort((mat[:,4],mat[:,1],mat[:,0]));
    smat = mat[ind];

    curr_L = mat[0,0];
    filepath = folderpath + str(curr_L) + ".dat";
    ofile = open(filepath,"w");
    startI = 0;
    for i in range(smat.shape[0]):
        if (smat[i,0] != curr_L):
            oneSize(smat[startI:i,:],temp,ofile);
            starI = i;
            curr_L = smat[i,0];
            filepath = folderpath+  str(curr_L) + ".dat";
            openfile =open(filepath,"w");
    oneSize(smat[startI:,:],temp,ofile);
            



        


