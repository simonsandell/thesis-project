import sys
import os
import numpy as np
import subprocess

from Ising3D import analyzeIsing3D as anaT
from Ising3D import L_analyzeIsing3D as anaL
import scalingCorr2L as anaSC2L
import scalingCorr3L as anaSC3L
#functions
from Ising3D import bin_omega_3L as SCbin3L
from Ising3D import bin_omega_2L as SCbin2L

import anaFuncs
import gps

arguments = sys.argv
doAnalysis = (arguments[1] == "1");
doPlot = (arguments[2] != "0");
outdir = "./foutput/Ising3D/"
if (doAnalysis):
    fName = arguments[3];
    datafile = open("./output/Ising3D/"+fName,"r");
    data = [];
    for ln in datafile:
        strlist = ln.rsplit(" ");
        strlist = [x for x in strlist if not (x== "\n")];
        fllist = [float(x) for x in strlist];
        data.append(fllist);
    dataMatrix = np.array(data);
    
    print("loading done, starting t data");
#    anaT.analyze(dataMatrix,fName);
    
    print("temp data done,starting l data");
 #   anaL.analyze(dataMatrix,fName);
    
    scalingDir = './foutput/Ising3D/scalingCorr';
    print("L data done, staring scaling corrections");
    
    dirname = scalingDir + "/omegaBin3L"
    anaSC3L.analyze(dataMatrix,dirname,SCbin3L.calcOmegaBin3L);
    print("3L Bin done");

    dirname = scalingDir + "/omegaBin2L"
    anaSC2L.analyze(dataMatrix,dirname,
            SCbin2L.calcOmegaBin2L,anaFuncs.getOmegaRange(-1.0,1.0,0.1));

    
if (doPlot):
    doPrint = (arguments[2] == "2");
    vstdir = outdir + "vsT/"
    for dirname in  os.listdir(vstdir):
        fullpath = os.path.join(vstdir,dirname);
        yaxis= anaFuncs.dirToYaxis(dirname);
        xaxis = "Temperature"
        title = "Ising3D_" + anaFuncs.dirToTitle(dirname)+ "_vs_" + xaxis;
        gps.graceDirPlot(fullpath,title,xaxis,yaxis,False,doPrint);
    vsldir = outdir + "vsL/"
    for dirname in  os.listdir(vsldir):
        fullpath = os.path.join(vsldir,dirname);
        yaxis= anaFuncs.dirToYaxis(dirname);
        xaxis = "L"
        title = "Ising3D_" + anaFuncs.dirToTitle(dirname)+ "_vs_" + xaxis;
        gps.graceDirPlot(fullpath,title,xaxis,yaxis,True,doPrint);
    scalingdir = outdir+"scalingCorr/"
    for dirname in os.listdir(scalingdir):
        fullpath= os.path.join(scalingdir,dirname)
        if ("3L" in fullpath):
            yaxis = anaFuncs.dirToYaxis(dirname);
            xaxis = "Temperature"
            title = "Ising3D_" + anaFuncs.dirToTitle(dirname) + "_vs_" + xaxis;
            gps.graceDirPlot(fullpath,title,xaxis,yaxis,False,doPrint);
    #    if ("2L" in dirpath):
    #        subprocess.call(["../scripts/omega_animation.sh",dirpath,"Ising3D_"+dirname])
