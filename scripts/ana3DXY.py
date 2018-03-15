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
from _3DXY import rhos_omega_3L as SCrhos3L
from _3DXY import rhos_omega_2L as SCrhos2L



def plot(directory,xaxis):
    subprocess.call(['../plot/reg_plot.sh',directory,xaxis]);
def logplot(directory,xaxis):
    subprocess.call(['../plot/log_plot.sh',directory,xaxis]);


outdir= "./foutput/3DXY/"
doAnalysis = True
doPlot = True
if (doAnalysis):
    arguments = sys.argv;
    fName = arguments[1];
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
    anaSC2L.analyze(dataMatrix,dirname,SCrhos2L.calcOmegaRS2L);
    
    print("2L RS done");
if (doPlot):
    vstdir = outdir + "vsT/"
    for dirname in  os.listdir(vstdir):
        print(os.path.join(vstdir,dirname))
        plot(os.path.join(vstdir,dirname),"Temperature");
    vsldir = outdir + "vsL/"
    for dirname in  os.listdir(vsldir):
        logplot(os.path.join(vsldir,dirname),"L");
    scalingdir = outdir+"scalingCorr/"
    for dirname in os.listdir(scalingdir):
        dirpath = os.path.join(scalingdir,dirname)
        if ("3L" in dirpath):
            plot(dirpath,"Temperature")
        if ("2L" in dirpath):
            subprocess.call(["../scripts/omega_animation.sh",dirpath])
