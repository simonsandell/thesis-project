import numpy as np
import settings
from plotting import fileWriter

for SKIP_N in range(4):
    result_struct = np.load("a_free_result_phenfit"+str(SKIP_N)+".npy")
    savePath = settings.foutput_path+settings.model + "/vsT/omega_fit/a_free_"
    savePathVar = settings.foutput_path+settings.model + "/vsT/omega_fit_var/a_free_"
    fileWriter.writeQuant(savePath+"omega_b_skip"+str(SKIP_N)+".dat", result_struct, [1, 2, 6]) # omega_bin
    fileWriter.writeQuant(savePath+"omega_r_skip"+str(SKIP_N)+".dat", result_struct, [1, 3, 8]) # omega_rho
    fileWriter.writeQuant(savePathVar+"var_omega_b_skip"+str(SKIP_N)+".dat", result_struct, [1, 4, 7]) # var_omega_bin
    fileWriter.writeQuant(savePathVar+"var_omega_r_skip"+str(SKIP_N)+".dat", result_struct, [1, 5, 9]) # var_omega_rho


