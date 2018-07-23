
import math
import numpy as np
import matplotlib.pyplot as plt

import settings


filelist = [
    np.load(settings.pickles_path + "correlation/" + settings.TAG + "4.npy"),
#    np.load(settings.pickles_path + "correlation/" + settings.TAG + "8.npy"),
#    np.load(settings.pickles_path + "correlation/" + settings.TAG + "16.npy"),
#    np.load(settings.pickles_path + "correlation/" + settings.TAG + "32.npy"),
#    np.load(settings.pickles_path + "correlation/" + settings.TAG + "64.npy"),
#    np.load(settings.pickles_path + "correlation/" + settings.TAG + "128.npy"),
]

datatables = [
    np.load(settings.DATATABLES[0]),
#    np.load(settings.DATATABLES[1]),
#g    np.load(settings.DATATABLES[2]),
#    np.load(settings.DATATABLES[3]),
#    np.load(settings.DATATABLES[4]),
#    np.load(settings.DATATABLES[5]),
]
# data format:
# L T xmag ymag time cluster_index

# definition of autocorrelation function:
# <A(0)A(t)> - <A^2>
T = filelist[0][0, 1]
Mags = []

for i in datatables:
    mag2 = i[60, 10]
    exp = i[60, 21]
    Mags.append(mag2/exp)
    print(Mags[-1])

def L_to_lidx(L):
    exp = math.log2(L)

    return int(exp -1.9)

def calc_mag(ser):
    # xmax = 2, ymag = 3
    xmag = ser[:, 2]
    ymag = ser[:, 3]
    L = ser[0, 0]
    Ls = L*np.ones(xmag.shape)

    return np.power(np.power(xmag, 2.0) + np.power(ymag, 2.0), 0.5)/np.power(Ls, 3)

def calc_corr(timeseries, step):
    mag_t = calc_mag(timeseries)
    L = timeseries[0,0]
    m2 =  Mags[L_to_lidx(L)]
    corr = mag_t[0:step:step]*mag_t[step::step]
    print(np.mean(corr))
    return (np.mean(corr)-m2), np.std(corr)

def calc_time(timeseries, step):
    res = []
    res[:] = []
    for t_1, t_2 in zip(timeseries[0:step:step, 4], timeseries[step::step, 4]):
        res.append(t_2-t_1)
    return np.mean(res), np.std(res)

correlation_func = []
N_com = int(filelist[0].shape[0]/2.0)
steprange= []

for i in range(1, 1000, 100):
    print(i )
    correlation_func.append([*calc_time(filelist[0], i), *calc_corr(filelist[0], i)])
corr_func = np.array(correlation_func)
plt.figure()
plt.errorbar(corr_func[:, 0],
        corr_func[:, 2],
        xerr=corr_func[:,1],
        yerr=corr_func[:,3],
        fmt='o')
plt.show()
