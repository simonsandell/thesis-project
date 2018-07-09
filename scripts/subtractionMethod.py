import numpy as np
import pandas as pd

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm

import settings
from plotting import fileWriter

def plot_results_two_l_log(res):
    a_num = np.unique(res[0, :, 0]).shape[0]
    curve_num = res.shape[0]
    temp_num = np.unique(res[0, :, 1]).shape[0]
    for a_idx in range(a_num):
        fig = plt.figure(figsize=(10, 8))
        for plane_idx  in range(curve_num):
            current_ln = res[plane_idx, a_idx*temp_num:(a_idx+1)*temp_num, :]
            x = res[plane_idx, a_idx*temp_num:(a_idx+1)*temp_num, 1]
            y = res[plane_idx, a_idx*temp_num:(a_idx+1)*temp_num, 4]
            lab = str(current_ln[0, :])
            plt.plot(x, y, label=lab)
        plt.legend()
        plt.show()


#
# A_r_guess = 1.115775
# A_b_guess = 1.24805


def calculate_omega(val_1, val_2, a_val):
    try:
        omega = -np.log((val_2 - a_val) / (val_1 - a_val)) / np.log(2) 
    except:
        return np.nan

    return omega


def get_bin_rho_omega(vals_l1, vals_l2, a_val):
    bin_val1 = vals_l1[22]
    bin_val2 = vals_l2[22]
    rho_val1 = vals_l1[26]
    rho_val2 = vals_l2[26]

    return [
        calculate_omega(bin_val1, bin_val2, a_val),
        calculate_omega(rho_val1, rho_val2, a_val),
    ]

if __name__ == '__main__':
    DATLIST = [
        np.load(settings.DATATABLES[0]),
        np.load(settings.DATATABLES[1]),
        np.load(settings.DATATABLES[2]),
        np.load(settings.DATATABLES[3]),
        np.load(settings.DATATABLES[4]),
        np.load(settings.DATATABLES[5]),
    ]
    JACKLIST = [
        np.load(settings.JACKTABLES[0]),
        np.load(settings.JACKTABLES[1]),
        np.load(settings.JACKTABLES[2]),
        np.load(settings.JACKTABLES[3]),
        np.load(settings.JACKTABLES[4]),
        np.load(settings.JACKTABLES[5]),
    ]
    TAG = "jul_5_zoom_1"
    JACK_NUM = JACKLIST[0].shape[0]
    # prune T's assuming they are temperature sorted...
    
    for DAT in DATLIST:
        DAT = DAT[50:76, :]
    
    for JDAT in JACKLIST:
        JDAT = JDAT[:, 50:76, :]
    
    a_values = np.linspace(1.24, 1.25, 100)
    NUM_SURF = len(DATLIST) - 1
    NUM_TEMP = DATLIST[0].shape[0]
    NUM_A = a_values.shape[0]
    NUM_values = 8
    results = np.empty((NUM_SURF, NUM_TEMP * NUM_A, NUM_values))
    # format  [ a , T , L1 , L2 , omega_b , omega_r , del_o_b , del_o_r ]
    
    
    for a_idx, a_const in enumerate(a_values):
        for t_idx in range(DATLIST[0].shape[0]):
            for l_idx in range(len(DATLIST) - 1):
                vals_1 = DATLIST[l_idx][t_idx, :]
                vals_2 = DATLIST[l_idx + 1][t_idx, :]
                j_vals_1 = JACKLIST[l_idx][:, t_idx, :]
                j_vals_2 = JACKLIST[l_idx + 1][:, t_idx, :]
                results[l_idx, a_idx * NUM_TEMP + t_idx, 0:4] = [
                    a_const,
                    vals_1[1],
                    vals_1[0],
                    vals_2[0],
                ]
                results[l_idx, a_idx * NUM_TEMP + t_idx, 4:6] = get_bin_rho_omega(
                    vals_1, vals_2, a_const
                )
    
                temporary_jack_res = np.empty((JACK_NUM, 2))
    
                for j_idx in range(JACK_NUM):
                    temporary_jack_res[j_idx, :] = get_bin_rho_omega(
                        j_vals_1[j_idx, :], j_vals_2[j_idx, :], a_const
                    )
                bin_delta = np.sqrt(JACK_NUM - 1) * np.std(temporary_jack_res[:, 0])
                rho_delta = np.sqrt(JACK_NUM - 1) * np.std(temporary_jack_res[:, 1])
                results[l_idx, a_idx * NUM_TEMP + t_idx, 6:] = [bin_delta, rho_delta]
    
    np.save(settings.pickles_path + "2L_log_omega/results_" + TAG, results)
    
    plot_results_two_l_log(results)
