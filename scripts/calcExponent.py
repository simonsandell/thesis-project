import numpy as np
import anaFuncs
import settings
import sys
from scipy.optimize import curve_fit
from plotting import fileWriter

omega = float(sys.argv[1]);
skip_n = int(sys.argv[2]);
if (settings.model == "3DXY"):
    idx = anaFuncs.get3DXYIndex();

def fitfunc(L,nu,a,b):
    res = (L**(1.0/nu))*(a + b*(L**(-omega)));
    return res;
def etafunc(L,eta,a,b):
    res = (L**(2-eta))*(a +b*(L**(-omega)));
    return res;

def calculateNu(tview):
    X = tview[:,0];
    Y = tview[:,idx["DBDT"][0]];
    params,covar = curve_fit(fitfunc,X,Y);
    res = np.empty((1,4));
    res[0,0] = tview[0,1];
    res[0,1] = params[0];
    res[0,2] = covar[0,0];
    res[0,3] = np.sum(tview[:,29]);
    return res;

def calculateEta(tview):
    X = tview[:,0];
    Y = tview[:,idx["CHI"][0]];
    params,covar = curve_fit(etafunc,X,Y);
    res = np.empty((1,4));
    res[0,0] = tview[0,1];
    res[0,1] = params[0];
    res[0,2] = covar[0,0];
    res[0,3] = np.sum(tview[:,29]);
    return res;
#  define some variables, path to datatables
dirpath = settings.root_path+"modular/datatables/combined/";
savename = "combined_omega_"+str(omega)+"_skip_"+str(skip_n);
filelist = [
        dirpath+"datatable_4combined3DXY.npy",
        dirpath+"datatable_8combined3DXY.npy",
        dirpath+"datatable_16combined3DXY.npy",
        dirpath+"datatable_32combined3DXY.npy",
        dirpath+"datatable_64combined3DXY.npy",
        dirpath+"datatable_128combined3DXY.npy"];
# skip first n datatables, then load remaining into all_tables
filelist = filelist[skip_n:];
asdf = np.load(filelist[0]);
shape = asdf.shape[1];
all_tables = np.empty((0,shape));
for f in filelist:
    dt = np.load(f);
    all_tables = np.append(all_tables,dt,axis=0);

#sort by temperature.
ind = np.lexsort((all_tables[:,0],all_tables[:,1]));
all_tables = all_tables[ind];
#temperatures unfortunately not exact, use some isclose magic to group unique temperatures
# into correct blocks
Tv,Ti = np.unique(all_tables[:,1],return_index=True);
Ti2 = Ti.copy();
for i in range(Ti.shape[0]-1):
    if (np.isclose(all_tables[Ti[i],1],all_tables[Ti[i+1],1],rtol=1e-10,atol=1e-10)):
        Ti2[i+1] = 0.0;
Ti = [x for x in Ti2 if not x == 0.0];
Ti = np.append(Ti,all_tables.shape[0]);
Ti = np.append(0,Ti);

result = np.empty((Ti.shape[0]-1,4));
eta_result = np.empty((Ti.shape[0]-1,4));
#result format : [T exponent var(exponent) N=NL1 + NL2]
for ind in range(Ti.shape[0]-1):
    tview = all_tables[Ti[ind]:Ti[ind+1],:];
    tview = tview[tview[:,0].argsort()];
    result[ind,:] = calculateNu(tview);
    eta_result[ind,:] = calculateEta(tview);
# write to dat files for plotting
writePath = settings.foutput_path+settings.model+"/vsT/nu/"+savename+".dat";
fileWriter.writeQuant(writePath,result,[0,1,2,3]);
eta_Path = settings.foutput_path+settings.model +"/vsT/eta/"+savename+".dat";
fileWriter.writeQuant(eta_Path,eta_result,[0,1,2,3]);
