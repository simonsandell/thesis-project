import sys
import os
import numpy as np
import subprocess

from _3DXY import analyze3DXY as anaT
from _3DXY import L_analyze3DXY as anaL
import scalingCorr2L as anaSC2L
import scalingCorr3L as anaSC3L 
#functions
from _3DXY import bin_omega_3L as SCbin3L
from _3DXY import bin_omega_2L as SCbin2L
from _3DXY import rhos_omega_3L as SCrhos3L
from _3DXY import rhos_omega_2L as SCrhos2L

import anaFuncs
import gps


arguments = sys.argv
doAnalysis = (arguments[1] == "1");
doPlot = (arguments[2] != "0");
outdir= "./foutput/3DXY/"
if (doAnalysis):
    fName = arguments[3];
    datafile = open("./output/3DXY/"+fName,"r");
    data = [];
    for ln in datafile:
        strlist = ln.rsplit(" ");
        strlist = [x for x in strlist if not (x== "\n")];
        fllist = [float(x) for x in strlist];
        data.append(fllist);
    dataMatrix = np.array(data);
    
    print("loading done, starting t data");
    anaT.analyze(dataMatrix,fName);
    
    print("temp data done,starting l data");
    anaL.analyze(dataMatrix,fName);
    
    scalingDir = './foutput/3DXY/scalingCorr';
    print("L data done, staring scaling corrections");
    dirname = scalingDir + "/omegaRS3L"
    anaSC3L.analyze(dataMatrix,dirname,SCrhos3L.calcOmegaRS3L);
    
    print("3L RS done");
    dirname = scalingDir + "/omegaBin3L"
    anaSC3L.analyze(dataMatrix,dirname,SCbin3L.calcOmegaBin3L);
    print("3L Bin done");

    dirname = scalingDir + '/omegaRS2L';
    anaSC2L.analyze(dataMatrix,dirname,
            SCrhos2L.calcOmegaRS2L,anaFuncs.getOmegaRange(0.0,1.0,0.05));

    print("2L RS done");

    dirname = scalingDir + '/omegaBin2L';
    anaSC2L.analyze(dataMatrix,dirname,
            SCbin2L.calcOmegaBin2L,anaFuncs.getOmegaRange(0.0,1.0,0.05));
    print("2L Bin done")
    
if (doPlot):
    doPrint = (arguments[2] == "2");
    vstdir = outdir + "vsT/"
    for dirname in  os.listdir(vstdir):
        fullpath = os.path.join(vstdir,dirname);
        yaxis= anaFuncs.dirToYaxis(dirname);
        xaxis = "Temperature"
        title = "3DXY_" + anaFuncs.dirToTitle(dirname)+ "_vs_" + xaxis;
        gps.graceDirPlot(fullpath,title,xaxis,yaxis,False,doPrint);
    vsldir = outdir + "vsL/"
    for dirname in  os.listdir(vsldir):
        fullpath = os.path.join(vsldir,dirname);
        yaxis= anaFuncs.dirToYaxis(dirname);
        xaxis = "L"
        title = "3DXY_" + anaFuncs.dirToTitle(dirname)+ "_vs_" + xaxis;
        gps.graceDirPlot(fullpath,title,xaxis,yaxis,True,doPrint);
    scalingdir = outdir+"scalingCorr/"
    for dirname in os.listdir(scalingdir):
        fullpath= os.path.join(scalingdir,dirname)
        if ("3L" in fullpath):
            yaxis = anaFuncs.dirToYaxis(dirname);
            xaxis = "Temperature"
            title = "3DXY_" + anaFuncs.dirToTitle(dirname) + "_vs_" + xaxis;
            gps.graceDirPlot(fullpath,title,xaxis,yaxis,False,doPrint);
        if ("2L" in fullpath):
            yaxis = anaFuncs.dirToYaxis(dirname);
            xaxis = "Temperature"
            title = "3DXY_" + anaFuncs.dirToTitle(dirname) + "_vs_" + xaxis;
            gps.graceAnimation(fullpath,title,xaxis,yaxis);
