import math
import numpy as np
from scipy.stats import binned_statistic
import matplotlib.pyplot as plt
import settings

filelist = [
    settings.pickles_path + "correlation/jack/jack_" + settings.TAG + "4.npy",
    settings.pickles_path + "correlation/jack/jack_" + settings.TAG + "8.npy",
    settings.pickles_path + "correlation/jack/jack_" + settings.TAG + "16.npy",
    settings.pickles_path + "correlation/jack/jack_" + settings.TAG + "32.npy",
    settings.pickles_path + "correlation/jack/jack_" + settings.TAG + "64.npy",
    settings.pickles_path + "correlation/jack/jack_" + settings.TAG + "128.npy",
]

best_data = [
    np.load(settings.DATATABLES[0]),
    np.load(settings.DATATABLES[1]),
    np.load(settings.DATATABLES[2]),
    np.load(settings.DATATABLES[3]),
    np.load(settings.DATATABLES[4]),
    np.load(settings.DATATABLES[5]),
]

#( 500, 10000, 7)
#( L, T, xmag, ymag, total_time, number of cluster, J_index)
def get_ms(subser):
    xmag2 = np.multiply(subser[:, :, 2], subser[:, :, 2])
    ymag2 = np.multiply(subser[:, :, 3], subser[:, :, 3])
    mag2 = np.add(xmag2, ymag2)
    mag = np.sqrt(mag2)
    avgm2 = np.mean(mag2.ravel())
    avgm = np.mean(mag.ravel())
    avgm2 /= math.pow(subser[0, 0, 0], 6)
    avgm /= math.pow(subser[0, 0, 0], 3)
    return avgm, avgm2

def get_ms_best(subser):
    L = subser[0, 0, 0]
    TOL = pow(10, -10)
    for bd in best_data:
        if abs(bd[0, 0] -L)< TOL:
            for ln in range(bd.shape[0]):
                if abs(bd[ln, 1] - 2.201840000)<TOL:
                    avgm = bd[ln, 9]
                    avgm2 = bd[ln, 10]
                    exp = bd[ln, 21]
                    break
    return avgm/exp, avgm2/exp


    


def get_M0MT(subser, d, am, am2):
    xmagprod = np.multiply(subser[:, d:, 2], subser[:, :-d, 2])
    ymagprod = np.multiply(subser[:, d:, 3], subser[:, :-d, 3])
    magprod = np.add(xmagprod, ymagprod)
    magprod = np.absolute(magprod)
    magprod = np.divide(magprod, math.pow(subser[0, 0, 0], 6))
    timediff = np.subtract(subser[:, d:, 4], subser[:, :-d, 4])
    timediff = np.divide(timediff, math.pow(subser[0, 0, 0], 3))
    return magprod.ravel(), timediff.ravel()


ndiffmax = [26, 51, 101, 201, 401, 801]
for l_idx, fname in enumerate(filelist):
    series = np.load(fname)
    series = series[300:305, :, :]
    avg_m, avg_m2 = get_ms_best(series)
    print('got avgs, m=',avg_m, ', m2=',avg_m2)
    print('C(0) = ', avg_m2 - pow(avg_m,2))
    correlations =[]
    correlations[:] =[]
    times = []
    times[:] = []
    #for diff in np.logspace(0.5, 3.3, 100):
    for diff in range(1, ndiffmax[l_idx]):
        print('diff: ', diff,'/',ndiffmax[l_idx]-1)
        c, t = get_M0MT(series, math.ceil(diff), avg_m, avg_m2)
        correlations.extend(c)
        times.extend(t)

    #times = np.array(times)
    #correlations = np.array(correlations)
    res, binedges, binnumber = binned_statistic(times, [times, correlations], statistic='mean', bins=1000)
    res[1] = res[1] - pow(avg_m, 2)
    res[1] /= (avg_m2 - pow(avg_m,2))
    np.save('binned'+str(4*pow(2,l_idx)), res)
    #plt.plot(res[0], res[1])/(avg_m2 - pow(avg_m,2)))
#plt.show() 
"""
    bins = np.linspace(0, max(correlations[:,0]), 500)
    inds = np.digitize(correlations[:, 0], bins])
    bin_means = [correlations[:,1
"""
