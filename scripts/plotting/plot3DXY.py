import settings
from plotting import gps
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
    called_dirs = set();
    for direc,subdir,files in os.walk(outdir):
        dop = False;
        for f in files:
            if ".dat" in f:
                dop = True;
        if (not direc in called_dirs) and dop and (dirfilt in direc):
            called_dirs.add(direc)
            parameters = anaFuncs.getParams(os.path.basename(direc),direc,doPrint);
            gps.graceDirPlot(*parameters,filefilt);
