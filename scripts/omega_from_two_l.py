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
    try:
        par, cov = curve_fit(fitfunc, x_val, y_val, sigma=dy_val)
    except:
        par = [np.nan, np.nan]
        cov = np.array(([[np.nan, np.nan], [np.nan, np.nan]]))
    return par, cov

SKIP_N = int(sys.argv[1])
TAG = settings.TAG + "_skip_" + repr(SKIP_N)
NAMELIST = [
    settings.pickles_path + "2Lquant/jul_26_final4_8.npy",
    settings.pickles_path + "2Lquant/jul_26_final8_16.npy",
    settings.pickles_path + "2Lquant/jul_26_final16_32.npy",
    settings.pickles_path + "2Lquant/jul_26_final32_64.npy",
    settings.pickles_path + "2Lquant/jul_26_final64_128.npy",
]
JACKLIST = [
    settings.pickles_path + "2Lquant/jackknife/jack_jul_26_final4_8.npy",
    settings.pickles_path + "2Lquant/jackknife/jack_jul_26_final8_16.npy",
    settings.pickles_path + "2Lquant/jackknife/jack_jul_26_final16_32.npy",
    settings.pickles_path + "2Lquant/jackknife/jack_jul_26_final32_64.npy",
    settings.pickles_path + "2Lquant/jackknife/jack_jul_26_final64_128.npy",
]
# format = [l1 , l2, t, b, rs, db, drs]
# remove SKIP_N smallest sizes
NAMELIST = NAMELIST[SKIP_N:]
JACKLIST = JACKLIST[SKIP_N:]
A = np.load(NAMELIST[0])
ALL_DT = np.empty((0, A.shape[1]))
J = np.load(JACKLIST[0])
N_JACK = J.shape[0]

N_FILES = len(JACKLIST)
N_TEMPS = J.shape[1]
N_JACKVALS = J.shape[2]
ALL_JACK = np.empty((N_JACK, N_FILES*N_TEMPS, N_JACKVALS))
# format: L1 L2 T B R dB dR
#        0  1  2 3 4 5  6  7  8
for ind, n in enumerate(NAMELIST):
    dt = np.load(n)
    ALL_DT = np.append(ALL_DT, dt, axis=0)
    jt = np.load(JACKLIST[ind])
    ALL_JACK[:, (ind*N_TEMPS):(ind+1)*N_TEMPS, :] = jt

# sort by temp
ALL_DT = ALL_DT[ALL_DT[:, 2].argsort()]
for i in range(N_JACK):
    view = ALL_JACK[i, :, :]
    sorted_view = view[view[:, 2].argsort()]
    ALL_JACK[i, :, :] = sorted_view

# pick out views of single T
TV, TI = np.unique(ALL_DT[:, 2], return_index=True)
TI2 = TI.copy()
for i in range(TI.shape[0] - 1):
    if np.isclose(ALL_DT[TI[i], 2], ALL_DT[TI[i + 1], 2], rtol=1e-10, atol=1e-10):
        TI2[i + 1] = 0.0
TI = [x for x in TI2 if not x == 0.0]
TI = np.append(TI, ALL_DT.shape[0])

# container for fit results
# [ T omega var(omega) jackknife(omega) ]
BIN_OMEGA = np.empty((TI.shape[0] - 1, 9))
RS_OMEGA = np.empty((TI.shape[0] - 1, 9))

# for each temperature, fit Q to powerlaw to obtain omega
for temp_ind in range(TI.shape[0] - 1):
    tview = ALL_DT[TI[temp_ind] : TI[temp_ind + 1], :]
    # sort view by L
    tview = tview[tview[:, 0].argsort()]
    # fit binder and rho quantity to power law to get omega
    # format = [l1 , l2, T, b, rs, db, drs]
    X = tview[:, 1]
    Yb = tview[:, 3]
    DYb = tview[:, 5]
    Yr = tview[:, 4]
    DYr = tview[:, 6]
    param, covar = fit_curve(X, Yb, DYb)
    BIN_OMEGA[temp_ind, :] = [tview[0, 2], param[0], param[1], covar[0, 0], covar[1, 1], 0.0, 0.0, 0.0, 0.0]
    param, covar = fit_curve(X, Yr, DYr)
    RS_OMEGA[temp_ind, :] = [tview[0, 2], param[0], param[1], covar[0, 0], covar[1, 1], 0.0, 0.0, 0.0, 0.0]
    jack_omega_bin = []
    jack_omega_bin[:] = []
    jack_omega_rs = []
    jack_omega_rs[:] = []
    jack_a_bin = []
    jack_a_bin[:] = []
    jack_a_rs = []
    jack_a_rs[:] = []
    jack_var_w_bin = []
    jack_var_w_bin[:] = []
    jack_var_w_rs = []
    jack_var_w_rs[:] = []
    jack_var_a_bin = []
    jack_var_a_bin[:] = []
    jack_var_a_rs = []
    jack_var_a_rs[:] = []
    for jack_i in range(N_JACK):
        X = ALL_JACK[jack_i, temp_ind*N_FILES:(temp_ind+1)*N_FILES:, 1]
        Yb = ALL_JACK[jack_i, temp_ind*N_FILES:(temp_ind+1)*N_FILES:, 3]
        Yr = ALL_JACK[jack_i, temp_ind*N_FILES:(temp_ind+1)*N_FILES:, 4]
        param, covar = fit_curve(X, Yb, DYb)
        jack_omega_bin.append(param[0])
        jack_a_bin.append(param[1])
        jack_var_w_bin.append(covar[0, 0])
        jack_var_a_bin.append(covar[1, 1])
        param, covar = fit_curve(X, Yr, DYr)
        jack_omega_rs.append(param[0])
        jack_a_rs.append(param[1])
        jack_var_w_rs.append(covar[0, 0])
        jack_var_a_rs.append(covar[1, 1])
    try:
        BIN_OMEGA[temp_ind, 5] = np.sqrt(len(jack_omega_bin) - 1) * np.std(jack_omega_bin)
        BIN_OMEGA[temp_ind, 6] = np.sqrt(len(jack_omega_bin) - 1) * np.std(jack_a_bin)
        BIN_OMEGA[temp_ind, 7] = np.sqrt(len(jack_omega_bin) - 1) * np.std(jack_var_w_bin)
        BIN_OMEGA[temp_ind, 8] = np.sqrt(len(jack_omega_bin) - 1) * np.std(jack_var_a_bin)
    except:
        print("asdf")
    try:
        RS_OMEGA[temp_ind, 5] = np.sqrt(len(jack_omega_rs) - 1) * np.std(jack_omega_rs)
        RS_OMEGA[temp_ind, 6] = np.sqrt(len(jack_omega_rs) - 1) * np.std(jack_a_rs)
        RS_OMEGA[temp_ind, 7] = np.sqrt(len(jack_omega_rs) - 1) * np.std(jack_var_w_rs)
        RS_OMEGA[temp_ind, 8] = np.sqrt(len(jack_omega_rs) - 1) * np.std(jack_var_a_rs)
    except:
        print("asdf_rs")

# disable warnings about invalid name
# pylint: disable=C0103
# plot
basep = settings.foutput_path +settings.model + "/2Lquant_fit/"
pth_omega_bin = basep + "omega_bin/" + str(SKIP_N) + TAG + ".dat"
pth_omega_rs = basep + "omega_rs/" + str(SKIP_N) + TAG + ".dat"
pth_a_bin = basep + "a_bin/" + str(SKIP_N) + TAG + ".dat"
pth_a_rs = basep + "a_rs/" + str(SKIP_N) + TAG + ".dat"
pth_var_omega_bin = basep + "var_omega_bin/" + str(SKIP_N) + TAG + ".dat"
pth_var_omega_rs = basep + "var_omega_rs/" + str(SKIP_N) + TAG + ".dat"
pth_var_a_bin = basep + "var_a_bin/" + str(SKIP_N) + TAG + ".dat"
pth_var_a_rs = basep + "var_a_rs/" + str(SKIP_N) + TAG + ".dat"
pth_a_omega_bin = basep + "a_omega_bin/" + str(SKIP_N) + TAG + ".dat"
pth_a_omega_rs = basep + "a_omega_rs/" + str(SKIP_N) + TAG + ".dat"
pth_var_bin = basep + "var_bin/" + str(SKIP_N) + TAG + ".dat"
pth_var_rs = basep + "var_rs/" + str(SKIP_N) + TAG + ".dat"
dirlist = [
    pth_omega_bin, pth_omega_rs, pth_a_bin, pth_a_rs,
    pth_var_omega_bin, pth_var_omega_rs, pth_var_a_bin, pth_var_a_rs,
    pth_a_omega_bin, pth_a_omega_rs, pth_var_bin, pth_var_rs,
]
for dir_paths in dirlist:
    d = os.path.dirname(dir_paths)
    if not os.path.exists(d):
        os.makedirs(d)

fileWriter.writeQuant(
    pth_omega_bin, BIN_OMEGA, [0, 1, 5]
    )
fileWriter.writeQuant(
    pth_a_bin, BIN_OMEGA, [0, 2, 6]
    )
fileWriter.writeQuant(
    pth_var_omega_bin, BIN_OMEGA, [0, 3, 7]
    )
fileWriter.writeQuant(
    pth_var_a_bin, BIN_OMEGA, [0, 4, 8]
    )

fileWriter.writeQuant(
    pth_omega_rs, RS_OMEGA, [0, 1, 5]
    )
fileWriter.writeQuant(
    pth_a_rs, RS_OMEGA, [0, 2, 6]
    )
fileWriter.writeQuant(
    pth_var_omega_rs, RS_OMEGA, [0, 3, 7]
    )
fileWriter.writeQuant(
    pth_var_a_rs, RS_OMEGA, [0, 4, 8]
    )
prod_BIN = BIN_OMEGA[:,:]
prod_RS = RS_OMEGA[:,:]
for temp_idx in range(BIN_OMEGA.shape[0]):
    T,w, a, VarW, VarA, dw, da, dVarW, dVarA = prod_BIN[temp_idx, :]

    prod_BIN[temp_idx, 1] = w*a
    prod_BIN[temp_idx, 2] = a*dw + w*da + da*dw
    prod_BIN[temp_idx, 3] = VarW + VarA
    prod_BIN[temp_idx, 4] = dVarW + dVarA

    T,w, a, VarW, VarA, dw, da, dVarW, dVarA = prod_RS[temp_idx, :]

    prod_RS[temp_idx, 1] = w*a
    prod_RS[temp_idx, 2] = a*dw + w*da + da*dw
    prod_RS[temp_idx, 3] = VarW + VarA
    prod_RS[temp_idx, 4] = dVarW + dVarA

fileWriter.writeQuant(
    pth_a_omega_bin, prod_BIN, [0, 1, 2]
    )
fileWriter.writeQuant(
    pth_var_bin, prod_BIN, [0, 3, 4]
    )
fileWriter.writeQuant(
    pth_a_omega_rs, prod_RS, [0, 1, 2]
    )
fileWriter.writeQuant(
    pth_var_rs, prod_RS, [0, 3, 4]
    )
