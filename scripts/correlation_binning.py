import math
import numpy as np
from scipy.stats import binned_statistic
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
for i,f in enumerate(filelist):
    filelist[i] = f[0:10, :, :]


#( 500, 10000, 7)
#( L, T, xmag, ymag, total_time, number of cluster, J_index)
def get_ms(subser):
    mag2 = subser[:, :, 2]*subser[:, :, 2] + subser[:, :, 3]*subser[:, :, 3]
    mag = np.power(mag2, 0.5*np.ones(mag2.shape))
    avgm2 = np.mean(mag2.ravel())
    avgm = np.mean(mag.ravel())
    return avgm, avgm2
    


def get_M0MT(subser, d, am, am2):
    magprod = abs(subser[:, d:, 2]*subser[:, :-d, 2] + subser[:, d:, 3]*subser[:, :-d, 3])
    magprod = subser[:, d:, 2]*subser[:, :-d, 2] + subser[:, d:, 3]*subser[:, :-d, 3]
    C = magprod - am*am
    c = C/(am2 - am*am)
    timediff = (subser[:, d:, 4] - subser[:, :-d, 4])/math.pow(subser[0, 0, 0], 3)
    return c.ravel(), timediff.ravel()


ndiffmax = [101, 201, 301, 401, 501, 601]
for l_idx, series in enumerate(filelist):
    avg_m, avg_m2 = get_ms(series)
    print('got avgs, m=',avg_m, ', m2=',avg_m2)
    correlations =[]
    times = []
    for diff in range(1, ndiffmax[l_idx]):
        print('diff: ', diff,'/',ndiffmax[l_idx]-1)
        c, t = get_M0MT(series, diff, avg_m, avg_m2)
        correlations.extend(c)
        times.extend(t)

    times = np.array(times)
    print(np.max(times))
    print(np.min(times))
    correlations = np.array(correlations)
    res, binedges, binnumber = binned_statistic(times, [times,correlations], statistic='mean', bins=np.arange(0, 10, 0.1))
    np.save('binned'+str(4*pow(2,l_idx)), res)
    plt.plot(res[0],res[1])
plt.show() 
"""
    bins = np.linspace(0, max(correlations[:,0]), 500)
    inds = np.digitize(correlations[:, 0], bins])
    bin_means = [correlations[:,1
"""
