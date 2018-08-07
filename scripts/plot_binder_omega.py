import os
import numpy as np
import matplotlib.pyplot as plt
def plt_eb(i1, i2, i3, data, lb):
    plt.errorbar(data[:, i1], data[:, i2], yerr=data[:, i3], label=lb)
def plt_eb_log(i1, i2, i3, data, lb):
    plt.yscale('log')
    plt.errorbar(data[:, i1], data[:, i2], yerr=data[:, i3], label=lb)


temperature = 1
omega_bin = 2
omega_rho = 3
var_omega_bin = 4
var_omega_rho = 5
delta_omega_bin = 6
delta_omega_rho = 7
delta_var_omega_bin = 8
delta_var_omega_rho = 9

for f in os.listdir("."):
    if "result_fit_omega" in f:
        result_struct = np.load(f)
        plt.figure()
        plt_eb(temperature, omega_bin, delta_omega_bin, result_struct, f)
        plt.show(block=False)
        plt.figure()
        plt_eb_log(temperature, var_omega_bin, delta_var_omega_bin, result_struct, f)
        plt.figlegend()
        plt.show()
