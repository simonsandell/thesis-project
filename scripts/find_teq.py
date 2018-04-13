import matplotlib.pyplot as plt

import numpy as np
import scipy.optimize as spo

#returns avg mag
def jfunc(mat):
    return [np.mean(mat[:,9])];

def writeLine(mat,avgN):
    avgM = jfunc(mat)[0];
    return [avgN,avgM];

#now we have data for only interesting temp, separete N_sweeps and print
def oneTemp(mat,nfac):
    result =[];
    startI = 0;
    high_N=4.0*nfac;
    avgPrev = 0.0;
    avgCurr = 0.0;
    for i in range(mat.shape[0]):
        if (mat[i,4]>high_N):
            avgCurr = np.mean(mat[startI:i,4]);
            result.append(writeLine(mat[startI:i],0.5*(avgCurr + avgPrev)));
            avgPrev = avgCurr;
            high_N= high_N*2;
            startI = i;
    avgCurr = np.mean(mat[startI:,4]);
    result.append(writeLine(mat[startI:,:],0.5*(avgCurr + avgPrev)));
    result = np.array(result);
    return result;


#we have block data for one L, pick out interesting temp.
def oneSize(mat,temp,betanu,z):
    #first, rescale mag and N
    for i in range(mat.shape[0]):
        mat[i,4] = mat[i,4]*pow(mat[i,0],-z);
        mat[i,9] = mat[i,9]*pow(mat[i,0],betanu);

    TOL = 0.000000005;
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
    ret = oneTemp(mat[startI:endI,:],pow(mat[i,0],-z));
    return ret;

#sort by L, then NTotSweeps
def analyze(mat,temp,betanu,z):
    ind = np.lexsort((mat[:,4],mat[:,1],mat[:,0]));
    smat = mat[ind];

    curr_L = mat[0,0];
    startI = 0;

    ret = [];
    for i in range(smat.shape[0]):
        if (smat[i,0] != curr_L):
            ret.append(oneSize(smat[startI:i,:],temp,betanu,z));
            startI = i;
            curr_L = smat[i,0];
    ret.append(oneSize(smat[startI:,:],temp,betanu,z));
    return ret;

def getDist(res):
    return np.std(res[:,0]) + np.std(res[:,1]) + np.std(res[:,2]);
    
def writeToFile(f,x,y):
    fstr= "{:30.30f}";
    f.write(fstr.format(x) + "    " + fstr.format(y) + "    0.0\n");
    
def matmax(mat):
    i,j = np.unravel_index(mat.argmax(),mat.shape);
    return mat[i,j];
def fit(params,X):
    a = params[0]
    b = params[1]
    c = params[2]
    return a*np.exp(b*X) + c;

def plot_comp(params,x,y):
    plt.scatter(x,y);
    X = np.geomspace(x[0],x[-1],20.0);
    Y = fit(params,X);
    plt.plot(X,Y,linewidth=2.0);

    
def findteq(mat,temp,betanu,path,drop_smallest,p):
    #plt.figure();
    f = open(path,"w");
    z = 0.0;
    dz = 0.1;
    while (z < 1.3): 
        if (z > 0.6):
            dz = 0.01;
        if (z > 1.15):
            dz = 0.1;
        rescaled = analyze(mat,temp,betanu,z);
        if (drop_smallest):
            del rescaled[0];
        res = [];
        res[:] = [];
        

        for j in range(len(rescaled)):
            x = rescaled[j][:,0];
            y = rescaled[j][:,1];
            #fit to exp funk
            print(rescaled[0])
            params,covars = spo.curve_fit(lambda t,a,b,c: a*np.exp(b*t) + c,x,y,p0=(p[0],p[1],p[2]),maxfev=2000);
            TOL = 10.0;
            if (matmax(covars) > TOL):
                print("bad fit")
            else:
                res.append(params);
        res = np.array(res);
        goodness = getDist(np.array(res));
        writeToFile(f,z,goodness);
        z = z+ dz;
        


