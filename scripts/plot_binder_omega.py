
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

import settings
result_struct = np.load("result_bin_fit_omega.npy")

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
