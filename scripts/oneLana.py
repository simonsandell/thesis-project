from multiprocessing import Pool
import numpy as np
import os
import math
import sys
import settings

from analysis import jackknife
from plotting import fileWriter
from plotting import datatableToPlots
from analysis import modelAvgs as ma

if (__name__=="__main__"):
    filepath = sys.argv[1];
    fName = os.path.basename(filepath).rstrip(".npy");
    model = settings.model;
    
    #data = pickler.loadData(model+filepath);
    data = np.load(filepath);
    #sort data
    
    ind= np.lexsort((data[:,1],data[:,0]));
    data = data[ind];
    
    
    def modelAvgs(avgs,mod=model):
        res = np.zeros(7);
        if (mod == "3DXY"):
            res[0] = ma.getBin(avgs[10],avgs[11],avgs[21])
            res[1] = ma.getC(avgs[7],avgs[8],avgs[21],avgs[1],math.pow(avgs[0],3));
            res[2] = ma.getChi(avgs[9],avgs[10],avgs[21],avgs[1],math.pow(avgs[0],3));
            res[3] = ma.getdBdT(avgs[10],avgs[11],avgs[12],avgs[13],avgs[7],avgs[21],avgs[1],math.pow(avgs[0],3));
            res[4] = ma.getRs(avgs[7],avgs[14],avgs[15],avgs[16],avgs[21],avgs[0],avgs[1]);
            res[5] = avgs[7]/avgs[21];
            res[6] = avgs[9]/avgs[21];
        return res;
    #calculate average of all columns, pass that to modelAvgs to obtain bin,dbdt,chi etc 
    #return nparray [avg(columns), modelAvgs(avgs)]
    def avgF(x):
        res = np.zeros(x.shape[1]);
        for i in range(x.shape[1]):
            res[i]= (np.mean(x[:,i]));
        modavgs = modelAvgs(res);
        res = np.append(res,modavgs);
        return res;
    #for a block with one T value 
    def calcForOneLOneT(view):
        avg = avgF(view);
        j_est = jackknife.jackknife(view,avgF,avg.shape[0]);
        t = repr(view[0,1]);
        l = repr(view[0,0]);
        np.save(settings.datatables_path+"jackknife/j_est_" + l+"_"+t,j_est);
        j_avg = np.mean(j_est,axis=0);
        j_std = np.std(j_est,axis=0);
        avg = np.append(avg,view.shape[0]);# add number of mcavgs to result
        j_delta = j_std*np.sqrt(j_est.shape[0]-1);
        avg = np.append(avg,j_delta);
        return avg;
    
    # find indices
    args = [];
    Lv,Li = np.unique(data[:,0],return_index=True);
    print(Lv)
    Li = np.append(Li,data.shape[0]);
    for l1,l2 in zip(Li[:-1],Li[1:]):
        Tv,Ti = np.unique(data[l1:l2,1],return_index=True);
        print(Tv)
        print(len(Tv));
        if (len(Tv) != 101):
            sys.exit(101);
        Ti = np.append(Ti,(l2-l1));
        for t1,t2 in zip(Ti[:-1],Ti[1:]):
            args.append(data[(l1+t1):(l1+t2),:]);
    print("number of jobs: " + str(len(args)));
    res = []
    nproc = 6;
    print("nproc="+str(nproc));
    pool = Pool(processes=nproc,maxtasksperchild=1);
    res.append(pool.map(calcForOneLOneT,args));
    pool.close()
    pool.join()
    res = np.array(res);
    res = res.squeeze();
    
    # save text file for visual inspeciton
    fileWriter.writeDataTable(fName,res);
    # save npy file for further analysis
    np.save(settings.datatables_path+"/datatable_"+fName+model,res);
    # make plots from  the npy datatables
    datatableToPlots.datatableToPlots(settings.datatables_path+"/",fName);
    
    
