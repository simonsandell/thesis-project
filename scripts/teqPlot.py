import jackknife

import numpy as np

#returns avg mag
def jfunc(mat):
    return [np.mean(mat[:,9])];

def writeLine(mat,openfile,avgN):
    avgM = jfunc(mat)[0];
    delM = jackknife.getJackDelta(mat,jfunc,100)[0];
    fstr= "{:30.30f}";
    openfile.write(fstr.format(avgN) + "    " + fstr.format(avgM) + "    " + fstr.format(delM) + "    " + str(mat.shape[0]) + "\n");

#now we have data for only interesting temp, separete N_sweeps and print
def oneTemp(mat,openfile):
    startI = 0;
    high_N=4.0;
    avgPrev = 0.0;
    avgCurr = 0.0;
    for i in range(mat.shape[0]):
        if (mat[i,4]>high_N):
            avgCurr = np.mean(mat[startI:i,4]);
            writeLine(mat[startI:i],openfile,0.5*(avgCurr + avgPrev));
            avgPrev = avgCurr;
            high_N= high_N*2;
            startI = i;
    avgCurr = np.mean(mat[startI:,4]);
    writeLine(mat[startI:,:],openfile,0.5*(avgCurr + avgPrev));

def printAll(mat,openfile):
    fstr= "{:30.30f}";
    for i in range(mat.shape[0]):
        openfile.write(fstr.format(mat[i,4]) + "    " + fstr.format(mat[i,9]) + "    " + fstr.format(0.0000)+ "     " + str(mat.shape[0]) + "\n");
        

#we have block data for one L, pick out interesting temp.
def oneSize(mat,temp,openfile):
    TOL = 0.000000005;
    startI = 0;
    endI = -1;
    for i in range(mat.shape[0]):
        if (abs(mat[i,1] - temp) < TOL):
            startI = i;
            endI = i;
            while True:
                if (abs(mat[endI,1] - temp)< TOL):
                    endI = endI +1;
                else:
                    break;
                if (endI == mat.shape[0]):
                    break;
            break;
    oneTemp(mat[startI:endI,:],openfile);
    #printAll(mat[startI:endI,:],openfile);

#sort by L, then NTotSweeps
def analyze(mat,folderpath,temp):
    ind = np.lexsort((mat[:,4],mat[:,1],mat[:,0]));
    smat = mat[ind];

    curr_L = mat[0,0];
    filepath = folderpath + str(int(curr_L)) + ".dat";
    ofile = open(filepath,"w");
    startI = 0;
    for i in range(smat.shape[0]):
        if (smat[i,0] != curr_L):
            oneSize(smat[startI:i,:],temp,ofile);
            startI = i;
            curr_L = smat[i,0];
            filepath = folderpath+  str(int(curr_L)) + ".dat";
            ofile =open(filepath,"w");
    oneSize(smat[startI:,:],temp,ofile);
            
