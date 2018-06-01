from plotting import fileWriter
import math
import settings
import numpy as np;
from scipy.optimize import curve_fit
import sys

def fitfunc(L,omega,a):
    res = a*(L**(-omega));
    return res;

skip_n = int(sys.argv[1])
namelist = [
        settings.pickles_path+"4.0_8.0_2Lquant.npy",
        settings.pickles_path+"8.0_16.0_2Lquant.npy",
        settings.pickles_path+"16.0_32.0_2Lquant.npy",
        settings.pickles_path+"32.0_64.0_2Lquant.npy",
        settings.pickles_path+"64.0_128.0_2Lquant.npy"];
#remove some
namelist = namelist[skip_n:];
a = np.load(namelist[0]);
all_dt = np.empty((0,a.shape[1]));
#format: L1 L2 T B R N1 N2 dB dR
#        0  1  2 3 4 5  6  7  8
for n in namelist:
    dt = np.load(n)
    all_dt = np.append(all_dt,dt,axis=0);
#sort by temp
all_dt = all_dt[all_dt[:,2].argsort()];

#pick out views of single T
Tv,Ti = np.unique(all_dt[:,2],return_index=True);
Ti2 = Ti.copy();
for i in range(Ti.shape[0]-1):
    if (np.isclose(all_dt[Ti[i],2],all_dt[Ti[i+1],2],rtol=1e-10,atol=1e-10)):
        Ti2[i+1] = 0.0;
Ti = [x for x in Ti2 if not x == 0.0];
Ti = np.append(Ti,all_dt.shape[0]);

#container for fit results
bin_omega = np.empty((Ti.shape[0]-1,4));
rs_omega = np.empty((Ti.shape[0]-1,4));


for ind in range(Ti.shape[0]-1):
    tview = all_dt[Ti[ind]:Ti[ind+1],:];
#sort view by L
    tview = tview[tview[:,0].argsort()];
#fit to power law to get omega
    X = tview[:,1];
    Yb = tview[:,3];
    Yr = tview[:,4];
    try:
        param,covar = curve_fit(fitfunc,X,Yb);
    except:
        param = ["nan"]
        covar =np.array(([["nan","nan"],["nan","nan"]]));
    bin_omega[ind,:] =[tview[0,2],param[0],covar[0,0],0.0];

    try:
        param,covar = curve_fit(fitfunc,X,Yr);
    except:
        param = ["nan"]
        covar =np.array(([["nan","nan"],["nan","nan"]]));
    rs_omega[ind,:] =[tview[0,2],param[0],covar[0,0],0.0];
#plot both omega as func of T
fileWriter.writeQuant(settings.foutput_path+settings.model+"/vsT/omega/bin"+str(skip_n)+".dat",bin_omega,[0,1,2,3])
fileWriter.writeQuant(settings.foutput_path+settings.model+"/vsT/omega/rs"+str(skip_n)+".dat",rs_omega,[0,1,2,3])
    
fileWriter.writeQuant(settings.foutput_path+settings.model+"/vsT/varomega/var_bin"+str(skip_n)+".dat",bin_omega,[0,2,3,3])
fileWriter.writeQuant(settings.foutput_path+settings.model+"/vsT/varomega/var_rs"+str(skip_n)+".dat",rs_omega,[0,2,3,3])

