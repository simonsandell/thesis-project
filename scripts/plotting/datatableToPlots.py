import numpy as np
import sys
import os
import settings
from plotting import fileWriter
import anaFuncs
np.set_printoptions(precision=13)
#load all datatables in one folder, combine, then do vsT and vsL plots
def datatableToPlots(folderName,tag):
    model = settings.model;
    allDT = np.empty((0,59));# all datatables
    for filename in os.listdir(folderName):
        if "datatable" in filename:
            datatable = np.load(os.path.join(folderName,filename));
            fileWriter.writeVsT(str(datatable[0,0])+"_"+tag,datatable)
            allDT = np.append(allDT,datatable,axis=0);
    # sort by T, then L 
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
        fileWriter.writeVsL(str(tview[0,1])+"_"+tag,tview);
    
def twoLtoPlot(path,savename):
    data = np.load(path);
    fileWriter.write2LData(savename,data);

