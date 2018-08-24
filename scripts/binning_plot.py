import matplotlib.pyplot as plt
import math
import numpy as np 
from plotting import fileWriter
import settings


def lidx_to_L(idx):
    return 4*math.pow(2, idx)

flist = [
        "./binned4.npy",
        "./binned8.npy",
        "./binned16.npy",
        "./binned32.npy",
        "./binned64.npy",
        "./binned128.npy"
        ]
plt.figure(num=1)
for li,f in enumerate(flist):
    cfunc = np.load(f)
    plt.plot(cfunc[0], cfunc[1], 'o-', label=f)
    print(cfunc[1, 0])
plt.yscale('log')
plt.figlegend()
plt.show()
path = settings.foutput_path + settings.model + "/vstime/corr/cf_"
fileWriter.writeQuant(path+str(lidx_to_L(li))+".dat", cfunc, [0, 2, 3, 1])
