import math
import time
import numpy as np
import matplotlib.pyplot as plt
import settings


filelist = [
    np.load(settings.pickles_path + "correlation/jack/jack_" + settings.TAG + "4.npy"),
    #np.load(settings.pickles_path + "correlation/jack/jack_" + settings.TAG + "8.npy"),
    #np.load(settings.pickles_path + "correlation/jack/jack_" + settings.TAG + "16.npy"),
    #np.load(settings.pickles_path + "correlation/jack/jack_" + settings.TAG + "32.npy"),
    #np.load(settings.pickles_path + "correlation/jack/jack_" + settings.TAG + "64.npy"),
    #np.load(settings.pickles_path + "correlation/jack/jack_" + settings.TAG + "128.npy"),
]



# data format:
# L T xmag ymag time cluster_index

# definition of autocorrelation function:
# <A(0)A(t)> - <A^2>

do_plot = False
Mags = []

def np_raise(numparr, exp):
    return np.power(numparr, exp*np.ones(numparr.shape))

def calc_mag(ser):
    # xmax = 2, ymag = 3
    xmag = ser[:, 2]
    ymag = ser[:, 3]
    L = ser[0, 0]
    # m = sqrt( xmag**2+ ymag**2)
    return np_raise(np_raise(xmag,2) + np_raise(ymag, 2), 0.5)

def calc_corr(mag_t, step, lidx, avg_m):
    #avg_m_sq = Mags[lidx]
    corr = []
    corr[:] = []
    corr = mag_t[:-step]*mag_t[step:] - (avg_m**2)
    return corr

def get_zero_corr(magser, avg_m):
    corr = []
    corr[:] = []
    corr = np.power(magser, 2*np.ones(magser.size)) - np.ones(magser.size)*(avg_m**2)
    return corr


def calc_MCS_per_clust(timeseries):
    diff = timeseries[1:, 4] - timeseries[:-1, 4] # diff is number of tested spinflips between clusters
    diff /= math.pow(timeseries[0, 0], 3)        #
    return diff

def calc_mag_sq(ser):
    return np.power(ser[:, 2], 2*np.ones(ser[:, 2].shape)) + np.power(ser[:, 3], 2*np.ones(ser[:, 3].shape))

print('done loading')
print(filelist[0].shape)

ndiffmax = np.linspace(100, 5000, 6)
for l_idx, series in enumerate(filelist):
    #begin by computing average time per cluster and <m>^2
    times = []
    times[:] = []
    for j in range(series.shape[0]):
        times.append(calc_MCS_per_clust(series[j, :, :]))
    times = np.array(times)
    avg_time = np.mean(times.ravel())
    delta_time = (1.0/pow(times.ravel().shape[0], 0.5))*np.std(times)
    print("computed avg_time")

    # compute magseries for each jack
    magseries = np.empty((series.shape[0], series.shape[1]))
    for j in range(series.shape[0]):
        magseries[j, :] = calc_mag(series[j, :, :])
    avg_mag = np.mean(magseries.ravel())

    # now do correlation function for range of times
    correlation_func = []
    correlation_func[:] = []
    zer_corr = []
    zer_corr[:] = []
    for j in range(series.shape[0]):
        zer_corr.append(get_zero_corr(magseries[j, :], avg_mag))
    correlation_func.append([0, 0, np.mean(zer_corr), 0])
    for ndiff in range(1, int(ndiffmax[l_idx])):
        print(ndiff+1, '/',ndiffmax[l_idx])
        curr_corr = []
        curr_corr[:] = []
        for j in range(series.shape[0]):
            curr_corr.append(calc_corr(magseries[j, :], ndiff, l_idx, avg_mag))
        avg_corr = np.mean(curr_corr)
        delta_corr = np.std(curr_corr)*(1.0/pow(len(curr_corr), 0.5))
        correlation_func.append([avg_time*ndiff, delta_time*ndiff, avg_corr, delta_corr])
    correlation_func = np.array(correlation_func)

    if do_plot:
            plt.figure()
            plt.errorbar(correlation_func[:, 0],
                         correlation_func[:, 2],
                         yerr=correlation_func[:, 3],
                         xerr=correlation_func[:, 1],
                         fmt='o')
            plt.show()
    np.save("new_correlation_func_" + repr(series[0, 0, 0]), correlation_func)
