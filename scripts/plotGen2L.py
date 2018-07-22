from plotting import fileWriter
import settings
import numpy as np


namelist = [
    settings.pickles_path + "/2Lquant/jul_204_8.npy",
    settings.pickles_path + "/2Lquant/jul_208_16.npy",
    settings.pickles_path + "/2Lquant/jul_2016_32.npy",
    settings.pickles_path + "/2Lquant/jul_2032_64.npy",
    settings.pickles_path + "/2Lquant/jul_2064_128.npy",
]
TAG = settings.TAG
a = np.load(namelist[0])
all_dt = np.empty((0, a.shape[1]))
# format: L1 L2 T B R  dB dR
#        0  1  2 3 4 5  6
for n in namelist:
    dt = np.load(n)
    all_dt = np.append(all_dt, dt, axis=0)
# sort by temp
all_dt = all_dt[all_dt[:, 2].argsort()]

# pick out views of single T
Tv, Ti = np.unique(all_dt[:, 2], return_index=True)
Ti2 = Ti.copy()
for i in range(Ti.shape[0] - 1):
    if np.isclose(all_dt[Ti[i], 2], all_dt[Ti[i + 1], 2], rtol=1e-10, atol=1e-10):
        Ti2[i + 1] = 0.0
Ti = [x for x in Ti2 if not x == 0.0]
Ti = np.append(Ti, all_dt.shape[0])


for ind in range(Ti.shape[0] - 1):
    tview = all_dt[Ti[ind] : Ti[ind + 1], :]
    # sort view by L
    tview = tview[tview[:, 0].argsort()]
    # print to files
    x = 0
    yb = 3
    dyb = 5
    yr = 4
    dyr = 6
    n = 5
    bpath = (
        settings.foutput_path
        + settings.model
        + "/vsL/2Lbin/"
        + TAG + "_"
        + str(tview[0, 2])
        + "_bin2L-binL.dat"
    )
    rpath = (
        settings.foutput_path
        + settings.model
        + "/vsL/2Lrs/"
        + TAG + "_"
        + str(tview[0, 2])
        + "_rs2L-rsL.dat"
    )
    fileWriter.writeQuant(bpath, tview, [x, yb, dyb, n])
    fileWriter.writeQuant(rpath, tview, [x, yr, dyr, n])
