import os
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import settings
datatables = [
    np.load(settings.DATATABLES[0]),
    np.load(settings.DATATABLES[1]),
    np.load(settings.DATATABLES[2]),
    np.load(settings.DATATABLES[3]),
    np.load(settings.DATATABLES[4]),
    np.load(settings.DATATABLES[5]),
]

Mags = []
Data = []

for i in datatables:
    mag = i[60, 28]
    Mags.append(math.pow(mag, 2))
    Data.append(i[60, :])

def plot_cf(cf):
    plt.figure()
    plt.plot(cf[:, 0], cf[:, 2])
    plt.show()

def lidx_to_L(idx):
    return 4*math.pow(2, idx)
def L_to_lidx(L):
    exp = math.log2(L)

    return int(exp -1.9)

def compute_clu_full(corr_func, L):
    s = 1.0
    ldata = Data[L]
    avg_m2 = ldata[21]/ldata[10]
    for k in range(corr_func.shape[0]):
        s += 2*(corr_func[k, 2])/avg_m2
    return s
def compute_clusts(corr_func, L):
    k = 0
    s = 1.0
    ldata = Data[L]
    avg_m2 = ldata[21]/ldata[10]
    while True:
        n = 2*(corr_func[k, 2])/avg_m2
        if n < 0:
            break
        s += n
        k += 1
        if k >= corr_func.shape[0]:
            print('not negative')
            break
    return s

corfunclist = [
    "./jack_correlation_func_4.0.npy",
    "./jack_correlation_func_8.0.npy",
    "./jack_correlation_func_16.0.npy",
    "./jack_correlation_func_32.0.npy",
    "./jack_correlation_func_64.0.npy",
    "./jack_correlation_func_128.0.npy",
]
result = []
for lidx, filenames in enumerate(corfunclist):
    corr_f = np.load(filenames)
    #n_clusts = compute_clusts(corr_f, lidx)
    n_clusts = compute_clu_full(corr_f, lidx)
    result.append([lidx_to_L(lidx), n_clusts*corr_f[1, 0]])
    print(filenames, n_clusts, n_clusts*corr_f[1, 0], corr_f[1, 0])
    """
    spectrum = np.fft.rfft(corr_f[:, 2])
    cspec = np.conj(spectrum)
    absspec = spectrum*cspec
    plt.figure()
    plt.plot(absspec)
    plt.show()
    """
    #plot_cf(corr_f)

result = np.array(result)
def func(x, a1, a2):
    return a1*np.power(x, a2);
p0 = [2.5, -0.1]
x = result[:, 0]
y = result[:, 1]
param, covar = curve_fit(func, x, y, maxfev=10000)

plt.figure()
#plt.yscale('log')
#plt.xscale('log')
plt.plot(result[:, 0], result[:,1])
xp = np.arange(0, 256, 1)
plt.plot(xp, func(xp, param[0], param[1]))
plt.show()


print(param,covar)
