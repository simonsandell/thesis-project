import matplotlib.pyplot as plt
import math
import numpy as np 
from plotting import fileWriter
import settings


def lidx_to_L(idx):
    return 4*math.pow(2, idx)

flist = [
        "./correlation_data/jack_correlation_func_4.0.npy",
        "./correlation_data/jack_correlation_func_8.0.npy",
        "./correlation_data/jack_correlation_func_16.0.npy",
        "./correlation_data/jack_correlation_func_32.0.npy",
        "./correlation_data/jack_correlation_func_64.0.npy",
        "./correlation_data/jack_correlation_func_128.0.npy",
        ]
for li,f in enumerate(flist):
    correlation_func = np.load(f)
    print(correlation_func.shape)
    print(correlation_func[-1, 1])
    if False:
        plt.figure()
        plt.errorbar(correlation_func[:, 0],
                     correlation_func[:, 2],
                     yerr=correlation_func[:, 3],
                     xerr=correlation_func[:, 1],
                     fmt='x'
                     )
        plt.show()
    path = settings.foutput_path + settings.model + "/vstime/corr/cf_"
    fileWriter.writeQuant(path+str(lidx_to_L(li))+".dat", correlation_func, [0, 2, 3, 1])
