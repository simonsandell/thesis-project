import sys
import os
from _3DXY import analyze3DXY as anaT
from _3DXY import L_analyze3DXY as anaL
import scalingCorr2L as anaSC2L
import scalingCorr3L as anaSC3L 
from _3DXY import bin_omega_3L as SCbin3L
from _3DXY import rhos_omega_3L as SCrhos3L
from _3DXY import rhos_omega_2L as SCrhos2L
import numpy as np
import subprocess


def plot(directory,xaxis):
    subprocess.call(['../plot/reg_plot.sh',directory,xaxis]);
def logplot(directory,xaxis):
    subprocess.call(['../plot/log_plot.sh',directory,xaxis]);



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
for dirname in  os.listdir('./foutput/3DXY/vsT'):
    plot(dirname,"Temperature");

print("temp data done,starting l data");
anaL.analyze(dataMatrix,fName);
for dirname in  os.listdir('./foutput/3DXY/vsL'):
    plot(dirname,"L");

scalingDir = './foutput/3DXY/scalingCorr';
print("L data done, staring scaling corrections");
dirname = scalingDir + '/omegaRS2L';
anaSC2L.analyze(dataMatrix,dirname,SCrhos2L.calcOmegaRS2L);

print("2L RS done");
dirname = scalingDir + "/omegaRS3L"
anaSC3L.analyze(dataMatrix,dirname,SCrhos3L.calcOmegaRS3L);

print("3L RS done");
dirname = scalingDir + "/omegaBin3L"
anaSC3L.analyze(dataMatrix,dirname,SCbin3L.calcOmegaBin3L);
print("3L Bin done");






