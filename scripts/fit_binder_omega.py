import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

import settings

# skip smallest
SKIP_N = 1
data = [np.load(x) for x in settings.DATATABLES[SKIP_N:]]
jack = [np.load(x) for x in settings.JACKTABLES[SKIP_N:]]

binderindex = 22
rhoindex = 26

NUM_T = data[0].shape[0]
NUM_J = jack[0].shape[0]

def fit_func(L, omega, b):
    a = 1.244
    return a + b*pow(L,-omega)

def perform_fit(data_list,t_idx, q_idx):
    X = []
    X[:] = []
    Y = []
    Y[:] = []
    for l_idx, ldata in enumerate(data_list):
        X.append(ldata[t_idx, 0])
        Y.append(ldata[t_idx, q_idx])
    params, covar = curve_fit(fit_func, X, Y )
    return params[0], covar[0, 0]

result_struct = np.empty((NUM_T, 20))
jack_result_struct = np.empty((NUM_J, NUM_T, 20))
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
    result_struct[t_idx, 6] = np.sqrt(NUM_J -1) * np.std(jack_res_struct[:, 0])
    result_struct[t_idx, 7] = np.sqrt(NUM_J -1) * np.std(jack_res_struct[:, 1])
    result_struct[t_idx, 8] = np.sqrt(NUM_J -1) * np.std(jack_res_struct[:, 2])
    result_struct[t_idx, 9] = np.sqrt(NUM_J -1) * np.std(jack_res_struct[:, 3])

np.save("result_bin_fit_omega_a_fix_skip_4", result_struct)

result_struct = np.load("result_bin_fit_omega_a_fix_skip_4.npy")

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
plt.show()
