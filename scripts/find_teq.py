import matplotlib.pyplot as plt
import cmath
import numpy as np
import scipy.stats as sps
import scipy.optimize as spo

#returns avg mag
def jfunc(mat):
    return [np.mean(mat[:,9])];

def writeLine(mat,avgN):
    avgM = jfunc(mat)[0];
    return [avgN,avgM];

#now we have data for only interesting temp, separete N_sweeps and print
def oneTemp(mat,nfac,z,betanu):

    #print(np.log(1/mat[-1,9])/np.log(mat[0,0]))
    #first, rescale mag and N
    for i in range(mat.shape[0]):
        mat[i,4] = mat[i,4]*pow(mat[i,0],-z);
        #mat[i,9] = mat[i,9]*pow(mat[i,0],betanu);
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
    for i in range(result.shape[0]):
        result[i,1] = result[i,1]/result[-1,1];
    return result;


#we have block data for one L, pick out interesting temp.
def oneSize(lmat,temp,betanu,z):
    startI = 0;
    endI = -1;
    TOL = 0.000005;
    i = 0;
    for i in range(lmat.shape[0]):
        if (abs(lmat[i,1] - temp) < TOL):
            startI = i;
            endI = i;
            while True:
                if (abs(lmat[endI,1] - temp)< TOL):
                    endI = endI +1;
                else:
                    break;
                if (endI == lmat.shape[0]):
                    break;
            break;
    ret = oneTemp(lmat[startI:endI,:],pow(lmat[i,0],-z),z,betanu);
    return ret;

#sort by L, then NTotSweeps
def analyze(tmat,temp,betanu,z):
    lv,li = np.unique(tmat[:,0],return_index=True);
    li = np.append(li,tmat.shape[0]);
    ret =[];
    for i in range(len(lv)):
        ret.append(oneSize(tmat[li[i]:li[i+1],:],temp,betanu,z));
    return ret;

#write output
def writeToFile(f,x,y):
    fstr= "{:30.30f}";
    f.write(fstr.format(x) + "    " + fstr.format(y) + "    0.0\n");
 
def fit(params,X):
    X = np.array(X);
    a = params[0]
    b = params[1]
    return   a*(1 -np.exp(b*X));

def plot_comp(params,xl,yl,Z):
    #plt.gca().set_xscale('log');
    for i in range(len(xl)):
        plt.plot(xl[i],yl[i]);
    #X = np.geomspace(pow(10,-3),x[-1],100.0);
    X = np.linspace(0,100,100.0);
    Y = fit(params,X);
    plt.plot(X,Y,linewidth=2.0);
    rlim = 100.0*pow(4.0,-Z);
    plt.gca().set_xlim(left=-5.0,right=rlim);

def chisquare(params,x,y):
    Y = fit(params,x);
    cs = sps.chisquare(y,Y);

    return cs[0];

def findteq(mat,fName,temp,betanu,path,drop_smallest,p):
    ind = np.lexsort((mat[:,4],mat[:,1],mat[:,0]));
    mat = mat[ind];
    #delrows = []
    #for i in range(mat.shape[0]):
    #    if (mat[i,4] > 1000.0 or mat[i,4] < 8):
    #        delrows.append(i);
    #mat = np.delete(mat,delrows,axis=0);
    #print(mat.shape)

    if (drop_smallest):
        fName = fName = "_drop_smallest";
    f = open(path+fName+".dat","w");
    z = 0.0;
    dz = 0.05;
    doPlot = input("Plot fit?");
    while (z < 2.0): 
        tempmat = np.empty_like(mat);
        tempmat[:] = mat;
        rescaled = analyze(tempmat,temp,betanu,z);
        if (drop_smallest):
            del rescaled[0];
            del rescaled[0];
        x = [];
        y = [];
        x[:] = [];
        y[:] = [];

        xl = [];
        yl = [];
        xl[:] = [];
        yl[:] = [];

        for j in range(len(rescaled)):
            xl.append(rescaled[j][:,0]);
            yl.append(rescaled[j][:,1]);
            x.extend(rescaled[j][:,0]);
            y.extend(rescaled[j][:,1]);
        #fit to exp func
        params,covars = spo.curve_fit(lambda t,a,b,: a*(1-np.exp(b*t)),x,y,p0=(p[0],p[1]),maxfev=2000);

        #plotting

        goodness = chisquare(params,x,y);
        writeToFile(f,z,goodness);
        z = z+ dz;
        
        if (doPlot == "Y"):
            plt.gca().set_title("z = " + str(z));
            plot_comp(params,xl,yl,z-dz);
            plt.show();


