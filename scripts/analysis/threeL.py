from multiprocessing import Pool
import math
import numpy as np
import settings
from analysis import jackknife
from plotting import fileWriter

def getBin(M2,M4,Exp):
    return M4*Exp/(M2*M2);

def getRS(e,sx,sy,sz,exp,L,T):
    rs = -L*e -(L*L*L*L/T)*(sx +sy +sz);
    rs = rs/(3.0*exp);
    return rs;

def calcOmegaFunc(view1,view2,view3):
    t= view1[0,1];
    l1=view1[0,0];
    l2=view2[0,0];
    l3=view3[0,0];
    b1 = getBin(np.mean(view1[:,10]),np.mean(view1[:,11]),np.mean(view1[:,21]));
    b2 = getBin(np.mean(view2[:,10]),np.mean(view2[:,11]),np.mean(view2[:,21]));
    b3 = getBin(np.mean(view3[:,10]),np.mean(view3[:,11]),np.mean(view3[:,21]));
    r1 = getRS(np.mean(view1[:,7]),np.mean(view1[:,14]),np.mean(view1[:,15]),np.mean(view1[:,16]),np.mean(view1[:,21]),l1,t);
    r2 = getRS(np.mean(view2[:,7]),np.mean(view2[:,14]),np.mean(view2[:,15]),np.mean(view2[:,16]),np.mean(view2[:,21]),l2,t);
    r3 = getRS(np.mean(view3[:,7]),np.mean(view3[:,14]),np.mean(view3[:,15]),np.mean(view3[:,16]),np.mean(view3[:,21]),l3,t);

    omegabin = -np.log((b3-b2)/(b2-b1));
    omegarho = -np.log((r3-r2)/(r2-r1));
    return [omegabin,omegarho];

#produce [T, omegabin, omegarho, L1,L2,L3,N1,N2,N3,domegabin,domegarho,]
def produceResults(arg):
    view1,view2,view3 = arg;
    omegabin,omegarho = calcOmegaFunc(view1,view2,view3);
    jomegas = jackknife.jackknife_3(view1,view2,view3,calcOmegaFunc,2,100);
    t = view1[0,1];
    l1 = view1[0,0];
    l2 = view2[0,0];
    l3 = view3[0,0];
    n1 = view1.shape[0];
    n2 = view2.shape[0];
    n3 = view3.shape[0];
    domegabin = np.sqrt(jomegas.shape[0]-1)*np.std(jomegas[:,0]);
    domegarho = np.sqrt(jomegas.shape[0]-1)*np.std(jomegas[:,1]);
    return [t,omegabin,omegarho,l1,l2,l3,n1,n2,n3,domegabin,domegarho];


def getTviews(mat):
    tv,ti = np.unique(mat[:,1],return_index=True);
    ti=np.append(ti,mat.shape[0]);
    res = [];
    for i,(tind1,tind2) in enumerate(zip(ti[:-1],ti[1:])):
        res.append(mat[tind1:tind2,:]);
    return res;

def threeLmethod(data1,data2,data3,model,savename):
    #entire datafiles for 3 systemsizes
    data1 = data1[data1[:,1].argsort()];
    data2 = data2[data2[:,1].argsort()];
    data3 = data3[data3[:,1].argsort()];
    l1,l2,l3 = data1[0,0],data2[0,0],data3[0,0];
    dat1views = getTviews(data1);
    dat2views = getTviews(data2);
    dat3views = getTviews(data3);
    result = []
    funcargs =[];

    for v1,v2,v3 in zip(dat1views,dat2views,dat3views):
        funcargs.append([v1,v2,v3]);
    nproc = 6;
    print("nproc="+str(nproc));
    pool = Pool(processes=nproc,maxtasksperchild=1);
    result =pool.map(produceResults,funcargs);
    pool.close()
    pool.join();
    fileWriter.writeThreeLMethod(savename+str(l1)+"_"+str(l2)+"_"+str(l3),model,result);
    return result;
