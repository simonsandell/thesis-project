import sys
import numpy as np
from scipy.optimize import curve_fit

from plotting import fileWriter
import settings

def fitfunc(size, omega, a_1):
    res = a_1 * (size ** (-omega))
    return res

def fit_curve(x_val, y_val):
    try:
        par, cov = curve_fit(fitfunc, x_val, y_val)
    except:
        par = ["nan"]
        cov = np.array(([["nan", "nan"], ["nan", "nan"]]))
    return par, cov

SKIP_N = int(sys.argv[1])
TAG = "jun_18"
NAMELIST = [
    settings.pickles_path + "2Lquant/jun_184_8.npy",
    settings.pickles_path + "2Lquant/jun_188_16.npy",
    settings.pickles_path + "2Lquant/jun_1816_32.npy",
    settings.pickles_path + "2Lquant/jun_1832_64.npy",
    settings.pickles_path + "2Lquant/jun_1864_128.npy",
]
JACKLIST = [
    settings.pickles_path + "2Lquant/jackknife/jack_jun_184_8.npy",
    settings.pickles_path + "2Lquant/jackknife/jack_jun_188_16.npy",
    settings.pickles_path + "2Lquant/jackknife/jack_jun_1816_32.npy",
    settings.pickles_path + "2Lquant/jackknife/jack_jun_1832_64.npy",
    settings.pickles_path + "2Lquant/jackknife/jack_jun_1864_128.npy"
]

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
BIN_OMEGA = np.empty((TI.shape[0] - 1, 4))
RS_OMEGA = np.empty((TI.shape[0] - 1, 4))

# for each temperature, fit Q to powerlaw to obtain omega
for temp_ind in range(TI.shape[0] - 1):
    tview = ALL_DT[TI[temp_ind] : TI[temp_ind + 1], :]
    # sort view by L
    tview = tview[tview[:, 0].argsort()]
    # fit binder and rho quantity to power law to get omega
    X = tview[:, 1]
    Yb = tview[:, 3]
    Yr = tview[:, 4]
    param, covar = fit_curve(X, Yb)
    BIN_OMEGA[temp_ind, :] = [tview[0, 2], param[0], covar[0, 0], 0.0]
    param, covar = fit_curve(X, Yr)
    RS_OMEGA[temp_ind, :] = [tview[0, 2], param[0], covar[0, 0], 0.0]
    jack_omega_bin = []
    jack_omega_bin[:] = []
    jack_omega_rs = []
    jack_omega_rs[:] = []
    for jack_i in range(N_JACK):
        X = ALL_JACK[jack_i, temp_ind*N_FILES:(temp_ind+1)*N_FILES:, 1]
        Yb = ALL_JACK[jack_i, temp_ind*N_FILES:(temp_ind+1)*N_FILES:, 3]
        Yr = ALL_JACK[jack_i, temp_ind*N_FILES:(temp_ind+1)*N_FILES:, 4]
        param, covar = fit_curve(X, Yb)
        jack_omega_bin.append(param[0])
        param, covar = fit_curve(X, Yr)
        jack_omega_rs.append(param[0])
    try:
        BIN_OMEGA[temp_ind, 3] = np.sqrt(len(jack_omega_bin) - 1) * np.std(jack_omega_bin)
    except:
        print("asdf")
    try:
        RS_OMEGA[temp_ind, 3] = np.sqrt(len(jack_omega_rs) - 1) * np.std(jack_omega_rs)
    except:
        print("asdf_rs")


# plot both omega as func of T
fileWriter.writeQuant(
    settings.foutput_path + settings.model + "/vsT/omega/bin" + str(SKIP_N) + TAG + ".dat",
    BIN_OMEGA,
    [0, 1, 3, 2]
)
fileWriter.writeQuant(
    settings.foutput_path + settings.model + "/vsT/omega/rs" + str(SKIP_N) + TAG + ".dat",
    RS_OMEGA,
    [0, 1, 3, 2]
)

fileWriter.writeQuant(
    settings.foutput_path
    + settings.model
    + "/vsT/varomega/var_bin"
    + str(SKIP_N)
    + TAG
    + ".dat",
    BIN_OMEGA,
    [0, 2, 3, 1]
)
fileWriter.writeQuant(
    settings.foutput_path
    + settings.model
    + "/vsT/varomega/var_rs"
    + str(SKIP_N)
    + TAG
    + ".dat",
    RS_OMEGA,
    [0, 2, 3, 1]
)
