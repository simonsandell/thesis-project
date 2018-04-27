import gps
import os
import anaFuncs

def plot3DXY():
    doPrint = input("save figures to eps?");
    if (doPrint == "y" or doPrint == "Y"):
        doPrint = True;
    else:
        doPrint = False;
    outdir = "./foutput/3DXY/";
    vstdir = outdir + "vsT/"
    vsldir = outdir + "vsL/"
    vsNdir = outdir+"vsN/";
    teqdir = outdir + "findZ/";
    scalingDir = outdir + "scalingCorr/";
    dirlist = [vstdir,vsldir,vsNdir,scalingDir,teqdir];
    for targetdir in dirlist:
        for dirname in  os.listdir(targetdir):
            fullpath = os.path.join(targetdir,dirname);
            parameters = anaFuncs.getParams(dirname,fullpath,doPrint);
            gps.graceDirPlot(*parameters);
