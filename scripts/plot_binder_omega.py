
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

import settings

def plt_eb(i1, i2, i3, data, lb):
    plt.errorbar(data[:, i1], data[:, i2], yerr=data[:, i3], label=lb)
def plt_eb_log(i1, i2, i3, data, lb):
    plt.yscale('log')
    plt.errorbar(data[:, i1], data[:, i2], yerr=data[:, i3], label=lb)

result_struct_1 = np.load("result_bin_fit_omega_a_fix_skip_4.npy")
result_struct_2 = np.load("result_bin_fit_omega_a_fix.npy")
result_struct_3 = np.load("result_bin_fit_omega.npy")
result_struct_4 = np.load("result_bin_fit_omega_a_free_skip_4.npy")

temperature =  1
omega_bin =  2
omega_rho =  3
var_omega_bin =  4
var_omega_rho =  5
delta_omega_bin =  6
delta_omega_rho =  7
delta_var_omega_bin =  8
delta_var_omega_rho =  9
plt.figure()
plt_eb(temperature, omega_bin, delta_omega_bin, result_struct_1, "w, a_fix_skip_4")
plt_eb(temperature, omega_bin, delta_omega_bin, result_struct_2, "w, a_fix")
plt_eb(temperature, omega_bin, delta_omega_bin, result_struct_3, "w, a free")
plt_eb(temperature, omega_bin, delta_omega_bin, result_struct_4, "w, a free skip 4")
plt.figlegend()
plt.show(block=False)
plt.figure()
plt_eb_log(temperature, var_omega_bin, delta_var_omega_bin, result_struct_1, "var(w), a_fix_skip_4")
plt_eb_log(temperature, var_omega_bin, delta_var_omega_bin, result_struct_2, "var(w), a_fix")
plt_eb_log(temperature, var_omega_bin, delta_var_omega_bin, result_struct_3, "var(w), a free")
plt_eb(temperature, var_omega_bin, delta_var_omega_bin, result_struct_4, "var(w), a free skip 4")
plt.figlegend()
plt.show()
