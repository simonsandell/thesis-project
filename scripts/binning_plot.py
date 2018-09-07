import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import settings
from plotting import fileWriter


def integrated_ctime(corfunc):
    stopi = 0
    for i in range(corfunc.shape[1]):
        if corfunc[1, i] < 0.0:
            stopi = i
            return np.trapz(corfunc[1, :stopi], corfunc[0, :stopi])
    if stopi == corfunc.shape[1]-1:
        for i in range(corfunc.shape[1]):
            if corfunc[0, i] < 0.0:
                stopi =i
                return np.trapz(corfunc[0, :stopi], corfunc[1, :stopi])
    return np.nan



def fitfunc(x, taup):
    return np.exp(-np.divide(x, taup))

def lidx_to_L(idx):
    return 4*math.pow(2, idx)

ss = './tbin/binned'
ss = './perclust/perclust_'
ss = './pertime/pertime_'
ss = './newrun_pertime/pertime_'
flist = [
    ss + "4.npy",
    ss + "8.npy",
    ss + "16.npy",
    ss + "32.npy",
    ss + "64.npy",
    #ss + "128.npy"
]

cutoffs = np.array([
    [15, 40],
    [15, 40],
    [15, 40],
    [15, 40],
    [15, 40],
])

plt.figure(num=1)
tau =[]
tau_2 =[]

for li,f in enumerate(flist):
    cfunc = np.load(f)
    print(cfunc.shape)
    cfunc[0, :] = np.divide(cfunc[0,: ],(lidx_to_L(li)**3))
    plt.plot(cfunc[0, :], cfunc[1,: ], 'o-', label=f)
    path = settings.foutput_path + settings.model + "/vstime/corr/cf_"
    fileWriter.writeQuant(path+str(lidx_to_L(li))+".dat", np.transpose(cfunc) , [0, 1, 1])
    # save times 5-30
    start_i = 0
    stop_i = 0

    for i in range(cfunc.shape[1]):
        if cfunc[0, i] < cutoffs[li, 0]:
            start_i = i

        if cfunc[0, i] > cutoffs[li, 1]:
            stop_i = i

            break

    params, covar = curve_fit(fitfunc, cfunc[0, start_i:stop_i], cfunc[1, start_i:stop_i])
    tau.append([4*pow(2, li), params[0]])
    tau_2.append([4*pow(2, li), integrated_ctime(cfunc)])

    path = settings.foutput_path + settings.model + "/vstime/corr/cf_"
    fileWriter.writeQuant(path+str(lidx_to_L(li))+".dat", np.transpose(cfunc), [0, 1])
tau = np.array(tau)
tau_2 = np.array(tau_2)
print(tau_2)

wp = settings.foutput_path + settings.model + "/vsL/tau/"
fileWriter.writeQuant(wp + "tau_fit.dat", tau, [0, 1])
fileWriter.writeQuant(wp + "tau_int.dat", tau_2, [0, 1])
"""
plt.yscale('log')
plt.figlegend()
plt.show()

print(tau_2)
plt.figure()
plt.plot(tau[:, 0], tau[:, 1])
plt.plot(tau_2[:, 0], tau_2[:, 1])
plt.yscale('log')
plt.xscale('log')
plt.show()
"""
