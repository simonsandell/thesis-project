import gps
import os
import anaFuncs
import settings


def plot3DXY():
    dirfilt = input("dir filter? ");
    filefilt = input("file filter? ");

    doPrint = input("save figures to eps? ");
    if (doPrint == "y" or doPrint == "Y"):
        doPrint = True;
    else:
        doPrint = False;
    outdir = settings.foutput_path+"3DXY/";
    vstdir = outdir + "vsT/"
    vsldir = outdir + "vsL/"
    vsNdir = outdir+"vsN/";
    teqdir = outdir + "findZ/";
    scalingDir = outdir + "scalingCorr/";
    dirlist = [vstdir,vsldir,vsNdir,scalingDir,teqdir];
    for targetdir in dirlist:
        for dirname in  os.listdir(targetdir):
            fullpath = os.path.join(targetdir,dirname);
            if (dirfilt in fullpath):
                parameters = anaFuncs.getParams(dirname,fullpath,doPrint);
                gps.graceDirPlot(*parameters,filefilt);
print(__name__)
if (__name__=="__main__"):
    plot3DXY();
