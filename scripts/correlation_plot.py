import matplotlib.pyplot as plt
import math
import numpy as np 
from plotting import fileWriter
import settings


def lidx_to_L(idx):
    return 4*math.pow(2, idx)

flist = [
        "./new_correlation_func_4.0.npy",
        "./new_correlation_func_8.0.npy",
        "./new_correlation_func_16.0.npy",
        "./new_correlation_func_32.0.npy",
        "./new_correlation_func_64.0.npy",
        "./new_correlation_func_128.0.npy",
        ]
plt.figure(num=1)
plt.yscale('log')
for li,f in enumerate(flist):
    cfunc = np.load(f)
   #plt.errorbar(cfunc[:, 0], cfunc[:, 2]/cfunc[0,2] ,yerr=cfunc[:, 3]/cfunc[0, 2], label=f)
    plt.plot(cfunc[:, 0], cfunc[:, 2]/cfunc[0,2] , 'o-', label=f)
    print(cfunc[1, 0])
plt.figlegend()
plt.show()
path = settings.foutput_path + settings.model + "/vstime/corr/cf_"
fileWriter.writeQuant(path+str(lidx_to_L(li))+".dat", cfunc, [0, 2, 3, 1])
