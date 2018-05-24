import numpy as np
import sys
import os
import settings
import fileWriter
np.set_printoptions(precision=13)
#load all datatables in one folder, combine, then do vsT and vsL plots
folderName= sys.argv[1];
model = sys.argv[2];
savename = sys.argv[3];
allDT = np.empty((0,59));
for filename in os.listdir(folderName):
    datatable = np.load(os.path.join(folderName,filename));
    fileWriter.writeVsT(savename,datatable)
    allDT = np.append(allDT,datatable,axis=0);

ind = np.lexsort((allDT[:,0],allDT[:,1]));
allDT = allDT[ind];
Tv,Ti = np.unique(allDT[:,1],return_index=True);
Ti2 = Ti.copy();
for i in range(Ti.shape[0]-1):
    if (np.isclose(allDT[Ti[i],1],allDT[Ti[i+1],1],rtol=1e-10,atol=1e-10)):
        Ti2[i+1] = 0.0;
Ti = [x for x in Ti2 if not x == 0.0];
Ti = np.append(Ti,allDT.shape[0]);
for ind in range(Ti.shape[0]-1):
    tview = allDT[Ti[ind]:Ti[ind+1],:];
    tview = tview[tview[:,0].argsort()];
    fileWriter.writeVsL(savename,tview);
    

