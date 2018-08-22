import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import settings
from plotting import fileWriter



def plot_cf(cf):
    plt.figure()
    plt.plot(cf[:, 0], cf[:, 2])
    plt.show()

# sum correlation function div by zcf until end of list
def compute_clu_full(corr_func, L):
    s = -1.0
    for k in range(corr_func.shape[0]):
        s += 2*(corr_func[k, 2]/corr_func[0, 2])

    return s

# sum correlation function div by zcf until negative term
def compute_clusts(corr_func, L):
    k = 0
    s = -1.0

    while True:
        n = 2*(corr_func[k, 2]/corr_func[0, 2])

        if n < 0:
            break
        s += n
        k += 1

        if k >= corr_func.shape[0]:
            print('not negative, L =', L)
            break

    return s

# format :   time, delta time, correlation_function, delta c_f
corfunclist = [
    "./new_correlation_func_4.0.npy",
    "./new_correlation_func_8.0.npy",
    "./new_correlation_func_16.0.npy",
    "./new_correlation_func_32.0.npy",
    "./new_correlation_func_64.0.npy",
    "./new_correlation_func_128.0.npy",
]
L_list = [4, 8, 16, 32, 64, 128];
result = []

for lidx, filenames in enumerate(corfunclist):
    corr_f = np.load(filenames)

    n_clusts = compute_clusts(corr_f, lidx)
    print('done reg')

    plus_cf = corr_f.copy()
    minus_cf = corr_f.copy()

    plus_cf[:, 2] = plus_cf[:, 2] + plus_cf[:, 3]
    minus_cf[:, 2] = minus_cf[:, 2] - minus_cf[:, 3]
    n_plus = compute_clu_full(plus_cf, lidx)
    n_minus = compute_clu_full(minus_cf, lidx)
    diffs = [abs(n_clusts - n_plus), abs(n_clusts - n_minus)]
    print('plusdiff, minusdiff', diffs)
    delta_n = max(diffs)
    result.append([L_list[lidx], n_clusts, delta_n*corr_f[1, 0]])
    print(L_list[lidx], n_clusts*corr_f[1, 0], delta_n*corr_f[1, 0])
    print('avg sweeps per cluster', corr_f[1, 0])
result = np.array(result)

#fit to powerlaw 
def func(ex, a1, a2):
    return a1*np.power(ex, a2)
p0 = [2.5, -0.1]
x = result[:, 0]
y = result[:, 1]
param, covar = curve_fit(func, x, y, sigma=result[:, 2], maxfev=10000)

plt.figure()
plt.yscale('log')
plt.xscale('log')
plt.errorbar(result[:, 0], result[:, 1], yerr=result[:, 2])
xp = np.arange(3, 156, 1)
fit = [xp, func(xp, param[0], param[1]), np.zeros(xp.shape)]
fit = np.transpose(np.array(fit))
plt.plot(fit[:, 0], fit[:, 1])
plt.show()
print(param, covar)
parameter_string = "# exponent:" + str(param[1]) + " var:" + str(covar[1, 1]) 
print(parameter_string)

wp = settings.foutput_path + settings.model + "/vsL/tau/"
fileWriter.writeQuant(wp + "tau.dat", result, [0, 1, 2])
fileWriter.writeQuant(wp + "fit.dat", fit, [0, 1, 2], parameter_string)
