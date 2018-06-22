import settings
from plotting import gps
import os
import anaFuncs
import settings

def two_last_dirs(directory):
    a = directory.rsplit("/")
    return a[-2] + "/" + a[-1]


def plot3DXY():
    dir_filt = input("dir filter? ")
    filefilt = input("file filter? ")
    inp_print = input("save figures to eps? ")
    do_print = bool(inp_print == "y" or inp_print == "Y")

    outdir = settings.foutput_path + "3DXY/"

    for direc, subdir, files in os.walk(outdir):
        if (subdir == [] and dir_filt in direc):
            print(two_last_dirs(direc))
            params = anaFuncs.plot_params(two_last_dirs(direc))
            gps.graceDirPlot(direc, params, do_print, filefilt)
