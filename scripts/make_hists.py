import os
import sys
from multiprocessing import Pool
import settings
from datahandle import textToFloats
from datahandle import hist_Nmcavg


# parallell script, loads all files in dir and converts to npy
# saves in settings.picklepath
TARGET_DIR = sys.argv[1]
if settings.model == "3DXY":
    nvals = 22
else:
    nvals = 19

RESULT = []
FILENAMES = sorted(os.listdir(TARGET_DIR))
NUM_FILES = len(FILENAMES)


def func(filename):
    if os.path.isfile(os.path.join(TARGET_DIR, filename)):
        ret = textToFloats.loadData(os.path.join(TARGET_DIR, filename), nvals)
        diffs = hist_Nmcavg.draw_diff_hist(ret)
        return [filename, max(diffs)]
    return ["nofile", 0]


pool = Pool(processes=4, maxtasksperchild=1)
RESULT = pool.map(func, FILENAMES)
pool.close()
pool.join()

resultfile = open(settings.datatables_path + "nmcavg_check.txt","a")
for x in RESULT:
    resultfile.write(x[0] + "       " + str(x[1]) + "\n")
