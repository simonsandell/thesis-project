import os
import numpy as np
import subprocess

from Ising3D import analyzeIsing3D as anaT
from Ising3D import L_analyzeIsing3D as anaL
import scalingCorr2L as anaSC2L
import scalingCorr3L as anaSC3L
import teqPlot as tp
#functions
from Ising3D import bin_omega_3L as SCbin3L
from Ising3D import bin_omega_2L as SCbin2L

import intersectOmega
import anaFuncs
import gps

#### settings ####


#################
def anaIsing3D(fName,doT,doL,doSC2,doSC3,doTeq,doAnalyze,doPlot,doPrint):
    doScaling = doSC2 or doSC3;
    outdir= "./foutput/Ising3D/"
    indir = "./output/Ising3D/"
    scalingDir = outdir + 'scalingCorr';
    if (doAnalyze):
        datafile = open(indir+fName,"r");
        data = [];
        for ln in datafile:
            strlist = ln.rsplit(" ");
            strlist = [x for x in strlist if not (x== "\n")];
            fllist = [float(x) for x in strlist];
            data.append(fllist);
        dataMatrix = np.array(data);
        print("loading done");
        if (doT):
            anaT.analyze(dataMatrix,fName);
            print("temp done");
        if (doL):
            anaL.analyze(dataMatrix,fName);
            print("L done");
        if (doSC3):
            dirname = scalingDir + "/omegaBin3L"
            anaSC3L.analyze(dataMatrix,dirname,SCbin3L.calcOmegaBin3L);
            print("3L Bin done");
        if (doSC2):
            dirname = scalingDir + '/omegaBin2L';
            anaSC2L.analyze(dataMatrix,dirname,
                SCbin2L.calcOmegaBin2L,anaFuncs.getOmegaRange(0.7,1.2,0.005));
            intersectOmega.sigmaIntersect(dirname);
            print("2L Bin done")
        if (doTeq):
            tp.analyze(dataMatrix,"./foutput/Ising3D/vsN/"+fName,4.50000000);
    if (doPlot):
        if (doT):
            vstdir = outdir + "vsT/"
            for dirname in  os.listdir(vstdir):
                fullpath = os.path.join(vstdir,dirname);
                yaxis= anaFuncs.dirToYaxis(dirname);
                xaxis = "Temperature"
                title = "Ising3D_" + anaFuncs.dirToTitle(dirname)+ "_vs_" + xaxis;
                gps.graceDirPlot(fullpath,title,xaxis,yaxis,False,False,doPrint);
        if (doL):
            vsldir = outdir + "vsL/"
            for dirname in  os.listdir(vsldir):
                fullpath = os.path.join(vsldir,dirname);
                yaxis= anaFuncs.dirToYaxis(dirname);
                xaxis = "L"
                title = "Ising3D_" + anaFuncs.dirToTitle(dirname)+ "_vs_" + xaxis;
                gps.graceDirPlot(fullpath,title,xaxis,yaxis,True,True,doPrint);
        if (doScaling):
            for dirname in os.listdir(scalingDir):
                fullpath= os.path.join(scalingDir,dirname)
                if ("3L" in fullpath and doSC3):
                    yaxis = anaFuncs.dirToYaxis(dirname);
                    xaxis = "Temperature"
                    title = "Ising3D_" + anaFuncs.dirToTitle(dirname) + "_vs_" + xaxis;
                    gps.graceDirPlot(fullpath,title,xaxis,yaxis,False,False,doPrint);
                if ("2L" in fullpath and "std" not in fullpath and doSC2 and doPrint):
                    yaxis = anaFuncs.dirToYaxis(dirname);
                    xaxis = "Temperature"
                    title = "Ising3D_" + anaFuncs.dirToTitle(dirname) + "_vs_" + xaxis;
                    gps.graceAnimation(fullpath,title,xaxis,yaxis);
                if (("std" in fullpath) and doSC2):
                    yaxis = anaFuncs.dirToYaxis(dirname);
                    xaxis = r"\xw\0";
                    title = anaFuncs.dirToTitle(dirname);
                    gps.graceDirPlot(fullpath,title,xaxis,yaxis,False,False,doPrint);
        if (doTeq):
            vsNdir = outdir+"vsN/";
            xaxis = "N\ssweeps\S"
            yaxis = "Magnetization"
            title = "Equilibration time study"
            gps.graceDirPlot(vsNdir,title,xaxis,yaxis,True,False,doPrint);
