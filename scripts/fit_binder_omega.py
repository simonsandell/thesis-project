import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from plotting import fileWriter

import settings

sp_fi = [0.8, -1.2]
sp_fr = [0.8, 1.1, -1.2]
# skip smallest
SKIP_N = int(sys.argv[1])
data = [np.load(x) for x in settings.DATATABLES[SKIP_N:]]
jack = [np.load(x) for x in settings.JACKTABLES[SKIP_N:]]

binderindex = 22
rhoindex = 26

NUM_T = data[0].shape[0]
NUM_J = jack[0].shape[0]

def fit_func_fix(L, omega, b):
    a = 1.244
    return a + b*pow(L, -omega)

def fit_func_free(L, omega, a, b):
    return a + b*pow(L, -omega)

def perform_fit(data_list, t_idx, q_idx):
    X = []
    X[:] = []
    Y = []
    Y[:] = []
    DY = []
    DY[:] = []
    for ldata in data_list:
        X.append(ldata[t_idx, 0])
        Y.append(ldata[t_idx, q_idx])
        DY.append(ldata[t_idx, q_idx +30])
    try:
        params, covar = curve_fit(fit_func_free, X, Y, p0=sp_fr, sigma=DY, maxfev=1000)
    except:
        params = [0]
        covar = np.zeros((1,1))
        print('reg fail')
    return params[0], covar[0, 0], DY

def perform_fit_jack(data_list, t_idx, q_idx, dy):
    X = []
    X[:] = []
    Y = []
    Y[:] = []
    for ldata in data_list:
        X.append(ldata[t_idx, 0])
        Y.append(ldata[t_idx, q_idx])
    try:
        params, covar = curve_fit(fit_func_free, X, Y, p0=sp_fr, sigma=dy, maxfev=10000)
    except:
        params = [0]
        covar = np.zeros((1,1))
        print('jack_fail')
    return params[0], covar[0, 0]

result_struct = np.zeros((NUM_T, 20))
for t_idx in range(NUM_T):
    omega_b, var_omb, DYB = perform_fit(data, t_idx, binderindex)
    #omega_r, var_omr, DYR = perform_fit(data, t_idx, rhoindex)
    omega_r, var_omr = 0.0, 0.0

    result_struct[t_idx, 0:6] = [
        data[0][t_idx, 0], data[0][t_idx, 1],
        omega_b, omega_r, var_omb, var_omr
    ] # min L, Temp, w_b, w_r, var(w_b), var(w_r)

    jack_res_struct = np.zeros((NUM_J, 4))
    for j_idx in range(NUM_J):
        one_jack = [x[j_idx, :, :] for x in jack]
        jack_res_struct[j_idx, :2] = perform_fit_jack(one_jack, t_idx, binderindex, DYB)
        #jack_res_struct[j_idx, 2:] = perform_fit_jack(one_jack, t_idx, rhoindex, DYR)
        #jack_res_struct[j_idx, :2] = 0.0, 0.0
        jack_res_struct[j_idx, 2:] = 0.0, 0.0
    result_struct[t_idx, 6] = np.sqrt(NUM_J -1) * np.std(jack_res_struct[:, 0])
    result_struct[t_idx, 7] = np.sqrt(NUM_J -1) * np.std(jack_res_struct[:, 1])
    result_struct[t_idx, 8] = np.sqrt(NUM_J -1) * np.std(jack_res_struct[:, 2])
    result_struct[t_idx, 9] = np.sqrt(NUM_J -1) * np.std(jack_res_struct[:, 3])
do_save = True
do_plot = False 
if do_save:
    np.save("a_free_result_phenfit"+str(SKIP_N), result_struct)
    savePath = settings.foutput_path+settings.model + "/vsT/omega_fit/a_free_"
    savePathVar = settings.foutput_path+settings.model + "/vsT/omega_fit_var/a_free_"
    fileWriter.writeQuant(savePath+"omega_b_skip"+str(SKIP_N)+".dat", result_struct, [1, 2, 6]) # omega_bin
    fileWriter.writeQuant(savePath+"omega_r_skip"+str(SKIP_N)+".dat", result_struct, [1, 3, 7]) # omega_rho
    fileWriter.writeQuant(savePathVar+"var_omega_b_skip"+str(SKIP_N)+".dat", result_struct, [1, 4, 8]) # var_omega_bin
    fileWriter.writeQuant(savePathVar+"var_omega_r_skip"+str(SKIP_N)+".dat", result_struct, [1, 5, 9]) # var_omega_rho


if do_plot:
    temperature = result_struct[:, 1]
    omega_bin = result_struct[:, 2]
    omega_rho = result_struct[:, 3]
    var_omega_bin = result_struct[:, 4]
    var_omega_rho = result_struct[:, 5]
    delta_omega_bin = result_struct[:, 6]
    delta_omega_rho = result_struct[:, 7]
    delta_var_omega_bin = result_struct[:, 8]
    delta_var_omega_rho = result_struct[:, 9]
    
    plt.figure()
    plt.errorbar(temperature, omega_bin, yerr=delta_omega_bin, label="w_b")
    plt.errorbar(temperature, omega_rho, yerr=delta_omega_rho, label="w_r")
    plt.figlegend()
    plt.show()
    plt.figure()
    plt.errorbar(temperature, var_omega_bin, yerr=delta_var_omega_bin, label="var(w_b)")
    plt.errorbar(temperature, var_omega_rho, yerr=delta_var_omega_rho, label="var(w_r)")
    plt.figlegend()
    plt.yscale('log')
    plt.show()
