from plotting import fileWriter
import settings
import numpy as np


namelist = [
    settings.pickles_path + "4.0_8.0_2Lquant.npy",
    settings.pickles_path + "8.0_16.0_2Lquant.npy",
    settings.pickles_path + "16.0_32.0_2Lquant.npy",
    settings.pickles_path + "32.0_64.0_2Lquant.npy",
    settings.pickles_path + "64.0_128.0_2Lquant.npy",
]
a = np.load(namelist[0])
all_dt = np.empty((0, a.shape[1]))
# format: L1 L2 T B R N1 N2 dB dR
#        0  1  2 3 4 5  6  7  8
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
    dyb = 7
    yr = 4
    dyr = 7
    n = 5
    bpath = (
        settings.foutput_path
        + settings.model
        + "/vsL/2Lbin/"
        + str(tview[0, 2])
        + "_bin2L-binL.dat"
    )
    rpath = (
        settings.foutput_path
        + settings.model
        + "/vsL/2Lrs/"
        + str(tview[0, 2])
        + "_rs2L-rsL.dat"
    )
    fileWriter.writeQuant(bpath, tview, [x, yb, dyb, n])
    fileWriter.writeQuant(rpath, tview, [x, yr, dyr, n])
