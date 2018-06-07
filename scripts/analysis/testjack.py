import random
import jackknife
import numpy as np


def jackfun(mat):
    avg = []
    for x in range(mat.shape[1]):
        avg.append(np.mean(mat[:, x]))
    return avg


randdata = []
err1 = []
err2 = []
for j in range(100):
    randdata[:] = []
    for i in range(100000):
        randdata.append([random.gauss(8.0, 0.4), random.gauss(23.0, 3.0)])
    datmat = np.array(randdata)
    err1.append(abs(np.mean(datmat[:, 0]) - 8.0))
    err2.append(abs(np.mean(datmat[:, 1]) - 23.0))
print(np.mean(err1))
print(np.mean(err2))
print(np.std(datmat[:, 0]) / pow(100000, 0.5))
print(np.std(datmat[:, 1]) / pow(100000, 0.5))
hopefullysigma = jackknife.getJackDelta(datmat, jackfun, 100)
print(hopefullysigma)
hopefullysigma = jackknife.getJackDelta(datmat, jackfun, 1000)
print(hopefullysigma)
hopefullysigma = jackknife.getJackDelta(datmat, jackfun, 10000)
print(hopefullysigma)
