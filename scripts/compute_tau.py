import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import settings
from plotting import fileWriter
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

# sum correlation function div by zcf until end of list
def compute_clu_full(corr_func, L):
    s = 1.0
    ldata = Data[L]
    avg_m2 = ldata[21]/ldata[10]

    for k in range(corr_func.shape[0]):
        s += 2*(corr_func[k, 2])/avg_m2

    return s

# sum correlation function div by zcf until negative term
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

# format :   time, delta time, correlation_function, delta c_f
corfunclist = [
    "./correlation_data/jack_correlation_func_4.0.npy",
    "./correlation_data/jack_correlation_func_8.0.npy",
    "./correlation_data/jack_correlation_func_16.0.npy",
    "./correlation_data/jack_correlation_func_32.0.npy",
    "./correlation_data/jack_correlation_func_64.0.npy",
    "./correlation_data/jack_correlation_func_128.0.npy",
]
result = []

for lidx, filenames in enumerate(corfunclist):
    corr_f = np.load(filenames)

    n_clusts = compute_clusts(corr_f, lidx)
    print('done reg')

    plus_cf = corr_f.copy()
    print('done plus')

    minus_cf = corr_f.copy()
    print('done minus')

    plus_cf[:, 2] = plus_cf[:, 2] + plus_cf[:, 3]
    minus_cf[:, 2] = minus_cf[:, 2] - minus_cf[:, 3]
    n_plus = compute_clusts(plus_cf, lidx)
    n_minus = compute_clusts(minus_cf, lidx)
    diffs = [abs(n_clusts - n_plus), abs(n_clusts - n_minus)]
    print('plusdiff, minusdiff', diffs)
    delta_n = max(diffs)
    result.append([lidx_to_L(lidx), n_clusts*corr_f[1, 0], delta_n*corr_f[1, 0]])
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
plt.errorbar(result[:, 0], result[:, 1], yerr= result[:, 2])
xp = np.arange(3, 156, 1)
fit = [xp, func(xp, param[0], param[1]), np.zeros(xp.shape)]
fit = np.transpose(np.array(fit))
plt.plot(fit[:, 0], fit[:, 1])
plt.show()
print(param, covar)
parameter_string = "# exponent:" + str(param[1]) + " var:" + str(covar[1, 1]) 

wp = settings.foutput_path + settings.model + "/vsL/tau/"
fileWriter.writeQuant(wp + "tau.dat", result, [0, 1, 2])
fileWriter.writeQuant(wp + "fit.dat", fit, [0, 1, 2], parameter_string)
