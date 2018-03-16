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


def plot(directory,xaxis):
    subprocess.call(['../plot/reg_plot.sh',directory,xaxis]);
def logplot(directory,xaxis):
    subprocess.call(['../plot/log_plot.sh',directory,xaxis]);


outdir= "./foutput/Ising3D/"
doAnalysis = True
doPlot = True
if (doAnalysis):
    arguments = sys.argv;
    fName = arguments[1];
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
