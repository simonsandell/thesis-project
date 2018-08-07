import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from plotting import fileWriter

import settings

spoint = [2.5, -1.2]
# skip smallest
SKIP_N = int(sys.argv[1])
data = [np.load(x) for x in settings.DATATABLES[SKIP_N:]]
jack = [np.load(x) for x in settings.JACKTABLES[SKIP_N:]]

binderindex = 22
rhoindex = 26

NUM_T = data[0].shape[0]
NUM_J = jack[0].shape[0]

def fit_func(L, omega, b):
    a = 1.244
    return a + b*pow(L, -omega)

def perform_fit(data_list, t_idx, q_idx):
    X = []
    X[:] = []
    Y = []
    Y[:] = []
    for ldata in data_list:
        X.append(ldata[t_idx, 0])
        Y.append(ldata[t_idx, q_idx])
    params, covar = curve_fit(fit_func, X, Y, p0=spoint, maxfev=5000)
    return params[0], covar[0, 0]

result_struct = np.empty((NUM_T, 20))
for t_idx in range(NUM_T):
    omega_b, var_omb = perform_fit(data, t_idx, binderindex)
    omega_r, var_omr = perform_fit(data, t_idx, rhoindex)

    result_struct[t_idx, 0:6] = [
        data[0][t_idx, 0], data[0][t_idx, 1],
        omega_b, omega_r, var_omb, var_omr
    ] # min L, Temp, w_b, w_r, var(w_b), var(w_r)

    jack_res_struct = np.empty((NUM_J, 4))
    for j_idx in range(NUM_J):
        one_jack = [x[j_idx, :, :] for x in jack]
        jack_res_struct[j_idx, :2] = perform_fit(one_jack, t_idx, binderindex)
        jack_res_struct[j_idx, 2:] = perform_fit(one_jack, t_idx, rhoindex)
        #jack_res_struct[j_idx, :2] = 0.0, 0.0
        #jack_res_struct[j_idx, 2:] = 0.0, 0.0
    result_struct[t_idx, 6] = np.sqrt(NUM_J -1) * np.std(jack_res_struct[:, 0])
    result_struct[t_idx, 7] = np.sqrt(NUM_J -1) * np.std(jack_res_struct[:, 1])
    result_struct[t_idx, 8] = np.sqrt(NUM_J -1) * np.std(jack_res_struct[:, 2])
    result_struct[t_idx, 9] = np.sqrt(NUM_J -1) * np.std(jack_res_struct[:, 3])
do_save = True
do_plot = False 
if do_save:
    np.save("result_fit_omega_skip_"+str(SKIP_N), result_struct)
    savePath = settings.foutput_path+settings.model + "/vsT/omega_fit/a_fix_"
    savePathVar = settings.foutput_path+settings.model + "/vsT/omega_fit_var/a_fix_"
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
