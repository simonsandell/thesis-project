import math
import numpy as np
import matplotlib.pyplot as plt
import settings



filelist = [
#   np.load(settings.pickles_path + "correlation/jack/jack_" + settings.TAG + "4.npy"),
#   np.load(settings.pickles_path + "correlation/jack/jack_" + settings.TAG + "8.npy"),
#   np.load(settings.pickles_path + "correlation/jack/jack_" + settings.TAG + "16.npy"),
#   np.load(settings.pickles_path + "correlation/jack/jack_" + settings.TAG + "32.npy"),
#   np.load(settings.pickles_path + "correlation/jack/jack_" + settings.TAG + "64.npy"),
   np.load(settings.pickles_path + "correlation/jack/jack_" + settings.TAG + "128.npy"),
]

datatables = [
#   np.load(settings.DATATABLES[0]),
#   np.load(settings.DATATABLES[1]),
#   np.load(settings.DATATABLES[2]),
#   np.load(settings.DATATABLES[3]),
#   np.load(settings.DATATABLES[4]),
   np.load(settings.DATATABLES[5]),
]

# data format:
# L T xmag ymag time cluster_index

# definition of autocorrelation function:
# <A(0)A(t)> - <A^2>

do_plot = False
Mags = []
Data = []

for i in datatables:
    mag = i[60, 28]
    Mags.append(math.pow(mag, 2))
    Data.append(i[60, :])

def calc_mag(ser):
    # xmax = 2, ymag = 3
    xmag = ser[:, 2]
    ymag = ser[:, 3]
    L = ser[0, 0]
    Ls = L*np.ones(xmag.shape)

    return np.power(np.power(xmag, 2.0) + np.power(ymag, 2.0), 0.5)/np.power(Ls, 3)

def calc_corr(timeseries, step, lidx):
    mag_t = calc_mag(timeseries)
    avg_m_sq = Mags[lidx]
    corr = []
    corr[:] = []
    corr = mag_t[0:-step:step]*mag_t[step::step]
    corr = corr - np.ones(corr.size)*avg_m_sq
    print(corr.shape)

    return corr

def calc_MCS_per_clust(timeseries):
    diff = timeseries[1::2, 4] - timeseries[:-1:2, 4]
    diff /= math.pow(timeseries[0, 0], 3)        #measure in sweeps

    return diff

#compute zerotime correlation function from datatables
def get_zero_corr(lidx):
    avg_m2 = Data[lidx][10]
    avg_m = Data[lidx][9]
    exp = Data[lidx][21]

    return avg_m2/exp - math.pow(avg_m/exp, 2)


JACK_N = filelist[0].shape[0]
TIME_N = filelist[0].shape[1]
print('done loading')

def jack_time(times):
    flt = np.ravel(times)
    res = []

    for ji in range(JACK_N):
        tmp1 = flt[:ji*TIME_N:]
        tmp2 = flt[(ji+1)*TIME_N:]
        res.append(np.mean(np.append(tmp1,tmp2)))

    return np.mean(flt), math.pow(JACK_N, 0.5)*np.std(res)


for l_idx, series in enumerate(filelist):
    #begin by computing average time per cluster
    times = []

    for j in range(JACK_N):
        times.append(calc_MCS_per_clust(series[j, :, :]))
    times = np.array(times)
    avg_time, delta_time = jack_time(times)
    print("computed avg_time")


    # now do correlation function for range of times
    correlation_func = []
    correlation_func[:] = []
    correlation_func.append([ 0, 0, get_zero_corr(l_idx), 0])

    for ndiff in range(1, 10000):
        curr_corr = []
        curr_corr[:] = []
        for j in range(JACK_N):
            curr_corr.append(calc_corr(series[j, :, :], ndiff, l_idx))
        curr_corr = np.array(curr_corr)
        correlation_func.append([avg_time*ndiff, delta_time*ndiff, *jack_time(curr_corr)])
    correlation_func = np.array(correlation_func)

    if do_plot:
            plt.figure()
            plt.errorbar(correlation_func[:, 0],
                         correlation_func[:, 2],
                         yerr=correlation_func[:, 3],
                         xerr=correlation_func[:, 1],
                         fmt='o')
            plt.show()
    np.save("jack_correlation_func_" + repr(series[0]), correlation_func)

