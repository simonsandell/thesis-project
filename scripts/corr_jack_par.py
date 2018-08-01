from multiprocessing import Pool
import math
import time
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

def calc_corr(mag_t, step, lidx):
    avg_m_sq = Mags[lidx]
    corr = []
    corr[:] = []
    corr = mag_t[:-step]*mag_t[step:]
    corr = corr - np.ones(corr.size)*avg_m_sq
    return corr


def calc_MCS_per_clust(timeseries):
    diff = timeseries[1:, 4] - timeseries[:-1, 4]
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
print(filelist[0].shape)

do_jack = True

def jack_time(times):
    t = time.time()
    block_size = times.shape[1]
    j_size = times.shape[0] -1
    if do_jack:
        jack_res = np.empty((JACK_N))
        out = np.empty((j_size, block_size), dtype=times.dtype)
        for ji in range(JACK_N):
            out[:ji, :] = times[:ji, :]
            out[ji:, :] = times[ji+1:, :]
            jack_res[ji] = np.mean(out)


        print(time.time() -t)
        return np.mean(times), math.pow(JACK_N, 0.5)*np.std(jack_res)
    else:
        print(time.time() - t)
        return np.mean(times), 0.0


for l_idx, series in enumerate(filelist):
    #begin by computing average time per cluster
    times = []

    for j in range(JACK_N):
        times.append(calc_MCS_per_clust(series[j, :, :]))
    times = np.array(times)
    avg_time, delta_time = jack_time(times)
    print("computed avg_time")

    # compute magseries for each jack
    magseries = np.empty((series.shape[0],series.shape[1]))
    for j in range(JACK_N):
        magseries[j, :] = calc_mag(series[j, :, :])

    # now do correlation function for range of times
    correlation_func = []
    correlation_func[:] = []
    correlation_func.append([ 0, 0, get_zero_corr(l_idx), 0])

    def compute_cf(ndiff):
        curr_corr = []
        curr_corr[:] = []
        for j in range(JACK_N):
            curr_corr.append(calc_corr(magseries[j, :], ndiff, l_idx))
        curr_corr = np.array(curr_corr)
        return [avg_time*ndiff, delta_time*ndiff, *jack_time(curr_corr)]

    ARGS = []
    RES = []
    for ndiff in range(1, 5000):
        ARGS.append(ndiff);
    POOL = Pool(processes=settings.nprocs, maxtasksperchild=1)
    RES.append(POOL.map(compute_cf, ARGS))
    POOL.close()
    POOL.join()
    correlation_func = np.array(RES)
    print(correlation_func.shape)
    correlation_func = np.squeeze(correlation_func)
    print(correlation_func.shape)
    ind = np.lexsort((correlation_func[:, 0],correlation_func[:, 1]))
    correlation_func = correlation_func[ind]

        #correlation_func.append([avg_time*ndiff, delta_time*ndiff, np.mean(curr_corr), (1/math.sqrt(JACK_N))*np.std(curr_corr)])
        

    if do_plot:
            plt.figure()
            plt.errorbar(correlation_func[:, 0],
                         correlation_func[:, 2],
                         yerr=correlation_func[:, 3],
                         xerr=correlation_func[:, 1],
                         fmt='o')
            plt.show()
    np.save("jack_correlation_func_" + repr(series[0,0,0]), correlation_func)

