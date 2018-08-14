import sys
import os
import numpy as np
from scipy.optimize import curve_fit

from plotting import fileWriter
import settings
def fitfunc(size, omega, a_1):
    res = a_1 * (size ** (-omega))
    return res

def fit_curve(x_val, y_val, dy_val):
    par, cov = curve_fit(fitfunc, x_val, y_val, sigma=dy_val, maxfev=200000)
    return par, cov


SKIP_N = int(sys.argv[1])
tmin,tmax = int(sys.argv[2]),int(sys.argv[3])

TAG = settings.TAG + "_skip_"
DATA = [
    np.load(settings.pickles_path + "2Lquant/jul_26_final4_8.npy"),
    np.load(settings.pickles_path + "2Lquant/jul_26_final8_16.npy"),
    np.load(settings.pickles_path + "2Lquant/jul_26_final16_32.npy"),
    np.load(settings.pickles_path + "2Lquant/jul_26_final32_64.npy"),
    np.load(settings.pickles_path + "2Lquant/jul_26_final64_128.npy"),
]
JACK = [
    np.load(settings.pickles_path + "2Lquant/jackknife/jack_jul_26_final4_8.npy"),
    np.load(settings.pickles_path + "2Lquant/jackknife/jack_jul_26_final8_16.npy"),
    np.load(settings.pickles_path + "2Lquant/jackknife/jack_jul_26_final16_32.npy"),
    np.load(settings.pickles_path + "2Lquant/jackknife/jack_jul_26_final32_64.npy"),
    np.load(settings.pickles_path + "2Lquant/jackknife/jack_jul_26_final64_128.npy"),
]


# format = [l1 , l2, t, b, rs, db, drs]
# remove SKIP_N smallest sizes
DATA = DATA[SKIP_N:]
JACK= JACK[SKIP_N:]
N_JACK = JACK[0].shape[0]
N_FILES = len(JACK)

#remove irrelevant temperatures
for x,y in enumerate(DATA):
    DATA[x] = y[tmin:tmax, :]
    JACK[x] = JACK[x][:, tmin:tmax, :]

N_TEMPS = DATA[0].shape[0]


BIN_RES = np.empty((N_TEMPS, 5))
RHO_RES = np.empty((N_TEMPS, 5))
# for each temperature, fit to powerlaw to obtain omega
for temp_ind in range(N_TEMPS):
    print(temp_ind +1 ,"/",N_TEMPS)
    tview = []
    tview[:] = []
    for x in DATA:
        tview.append(x[temp_ind, :])
    tview = np.array(tview)

    # fit binder and rho quantity to power law to get omega
    # format = [l1 , l2, T, b, rs, db, drs]
    X = tview[:, 1]
    Yb = tview[:, 3]
    DYb = tview[:, 5]
    Yr = tview[:, 4]
    DYr = tview[:, 6]
    param, covar = fit_curve(X, Yb, DYb)
    BIN_RES[temp_ind, :] = [tview[0, 2], param[0], covar[0, 0], 0.0, 0.0]
    param, covar = fit_curve(X, Yr, DYr)
    RHO_RES[temp_ind, :] = [tview[0, 2], param[0], covar[0, 0], 0.0, 0.0]

    jackres = np.empty((N_JACK, 4))
    for jack_i in range(N_JACK):
        jview = []
        jview[:] = []
        for x in JACK:
            jview.append(x[jack_i, temp_ind, :])
        jview = np.array(jview)
        Jb = jview[:, 3]
        Jr = jview[:, 4]
        param, covar = fit_curve(X, Jb, DYb)
        jackres[jack_i, :2] = param[0], covar[0,0]

        param, covar = fit_curve(X, Jr, DYr)
        jackres[jack_i, 2:] = param[0], covar[0,0]
    jackres = np.array(jackres)
    BIN_RES[temp_ind, 3] = np.sqrt(N_JACK) * np.std(jackres[:, 0])
    BIN_RES[temp_ind, 4] = np.sqrt(N_JACK) * np.std(jackres[:, 1])
    RHO_RES[temp_ind, 3] = np.sqrt(N_JACK) * np.std(jackres[:, 2])
    RHO_RES[temp_ind, 4] = np.sqrt(N_JACK) * np.std(jackres[:, 3])
    np.save('2lfit_binres_skip_'+str(SKIP_N),BIN_RES)
    np.save('2lfit_rhores_skip_'+str(SKIP_N),RHO_RES)

# disable warnings about invalid name
# pylint: disable=C0103
# plot
basep = settings.foutput_path +settings.model + "/2Lquant_fit/"
pth_omega_bin = basep + "omega_bin/" + str(SKIP_N) + TAG + ".dat"
pth_omega_rs = basep + "omega_rs/" + str(SKIP_N) + TAG + ".dat"
pth_var_omega_bin = basep + "var_omega_bin/" + str(SKIP_N) + TAG + ".dat"
pth_var_omega_rs = basep + "var_omega_rs/" + str(SKIP_N) + TAG + ".dat"
dirlist = [pth_omega_bin, pth_omega_rs, pth_var_omega_bin, pth_var_omega_rs]
for dir_paths in dirlist:
    d = os.path.dirname(dir_paths)
    if not os.path.exists(d):
        os.makedirs(d)
fileWriter.writeQuant(pth_omega_bin, BIN_RES, [0, 1, 3])
fileWriter.writeQuant(pth_var_omega_bin, BIN_RES, [0, 2, 4])
fileWriter.writeQuant(pth_omega_rs, RHO_RES, [0, 1, 3])
fileWriter.writeQuant(pth_var_omega_rs, RHO_RES, [0, 2, 4])
