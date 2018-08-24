import matplotlib.pyplot as plt
import math
import numpy as np 
from plotting import fileWriter
import settings


def lidx_to_L(idx):
    return 4*math.pow(2, idx)

ss = './perclust/perclust_'
ss = './pertime/pertime_'
ss = './tbin/binned'
flist = [
        ss + "4.npy",
        ss + "8.npy",
        ss + "16.npy",
        ss + "32.npy",
        ss + "64.npy",
        ss + "128.npy"
        ]
plt.figure(num=1)
for li,f in enumerate(flist):
    cfunc = np.load(f)
    print(cfunc.shape)
    #cfunc[0, : ] = np.divide(cfunc[0,: ],(lidx_to_L(li)**3))
    plt.plot(cfunc[0, :], cfunc[1,: ], 'o-', label=f)
    path = settings.foutput_path + settings.model + "/vstime/corr/cf_"
    fileWriter.writeQuant(path+str(lidx_to_L(li))+".dat", np.transpose(cfunc) , [0, 1, 1])
#plt.yscale('log')
plt.figlegend()
plt.show()
