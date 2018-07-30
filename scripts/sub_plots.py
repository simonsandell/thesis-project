import numpy as np
import settings
from plotting import fileWriter

def save_to_dat(res, name):
    temp_num = np.unique(res[0, :, 1]).shape[0]
    res = res[:, temp_num:(2*temp_num), :]
    curve_num = res.shape[0]
    bp = settings.foutput_path + '3DXY/vsT/A_variation/' + settings.TAG
    for plane_idx  in range(curve_num):
        curve_arr = res[plane_idx, :, :]
        fileWriter.writeQuant(bp + name +str(plane_idx)+'.dat', curve_arr, [1, 4, 6, 0, 2, 3, 5, 7 ])

filelist = [
    np.load(settings.pickles_path + "2L_log_omega/results_u4_skip_0.npy"),
    np.load(settings.pickles_path + "2L_log_omega/results_u4_skip_4.npy"),
    np.load(settings.pickles_path + "2L_log_omega/results_u4_skip_4_8.npy"),
    np.load(settings.pickles_path + "2L_log_omega/results_u4_skip_128.npy"),
    np.load(settings.pickles_path + "2L_log_omega/results_u4_skip_4_128.npy"),
]
names = [
    'u4_skip_0',
    'u4_skip_4',
    'u4_skip_4_8',
    'u4_skip_128',
    'u4_skip_4_128',
]

for eff, n in zip(filelist, names):
    save_to_dat(eff, n)
