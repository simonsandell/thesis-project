
import math
import numpy as np
import matplotlib.pyplot as plt

import settings


filelist = [
    np.load(settings.pickles_path + "correlation/jack/jack_" + settings.TAG + "4.npy"),
    np.load(settings.pickles_path + "correlation/jack/jack_" + settings.TAG + "8.npy"),
    np.load(settings.pickles_path + "correlation/jack/jack_" + settings.TAG + "16.npy"),
    np.load(settings.pickles_path + "correlation/jack/jack_" + settings.TAG + "32.npy"),
    np.load(settings.pickles_path + "correlation/jack/jack_" + settings.TAG + "64.npy"),
    np.load(settings.pickles_path + "correlation/jack/jack_" + settings.TAG + "128.npy"),
]

datatables = [
    np.load(settings.DATATABLES[0]),
    np.load(settings.DATATABLES[1]),
    np.load(settings.DATATABLES[2]),
    np.load(settings.DATATABLES[3]),
    np.load(settings.DATATABLES[4]),
    np.load(settings.DATATABLES[5]),
]
# data format:
# L T xmag ymag time cluster_index

# definition of autocorrelation function:
# <A(0)A(t)> - <A^2>

do_plot = False
T = filelist[0][0, 0, 1]
Mags = []
Data = []

def lidx_to_L(idx):
    return 4*math.pow(2, idx)

for i in datatables:
    mag = i[60, 28]
    Mags.append(math.pow(mag, 2))
    Data.append(i[60, :])

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

def calc_corr(timeseries, step, lidx):
    jlist = []
    for j in range(timeseries.shape[0]):
        mag_t = calc_mag(timeseries)
        avg_m_sq = Mags[lidx]
        corr = mag_t[0:-step:step]*mag_t[step::step]
        corr = corr - np.ones(corr.size)*avg_m_sq

        jlist.append(np.mean(corr))

#compute average time per cluster
def calc_MCS_per_clust(timeseries):
    diff = [];

    for j in range(timeseries.shape[0]):
        diff.append(timeseries[j, 1::2, 4] - timeseries[j, :-1:2, 4])
    atpc = np.mean(diff)
    delta_atpc = math.pow(timeseries.shape[0],0.5)*np.std(diff)
    atpc /= math.pow(timeseries[0, 0, 0], 3)        #measure in sweeps
    delta_atpc /= math.pow(timeseries[0, 0, 0], 3)
    return atpc, delta_atpc

#compute corrfunc at t=0 from MC avgs
def calc_corr_zero(lidx):
    avg_m2 = Data[lidx][10]
    avg_m = Data[lidx][9]
    exp = Data[lidx][21]
    return avg_m2/exp  - math.pow(avg_m/exp,2)


for l_idx, series in enumerate(filelist):
    correlation_func = []
    correlation_func[:] = []
    correlation_func.append([ 0, 0, calc_corr_zero(l_idx), 0])

    avg_time, delta_time = calc_MCS_per_clust(series)
    print('average cluster time ', avg_time)
    print('average m2', Mags[l_idx])

    # for timediffs of upto x, compute correlation function
    for i in range(1, 500):
        correlation_func.append([i*avg_time[0], i*avg_time[1], *calc_corr(series, i, l_idx)])
    corr_func = np.array(correlation_func)
    if do_plot:
        plt.figure()
        plt.errorbar(corr_func[:, 0],
                     corr_func[:, 2],
                     fmt='o')
        plt.show()
    np.save("corr_func_" + repr(lidx_to_L(l_idx)), corr_func)
