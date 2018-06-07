import sys
import os
import numpy as np
from analysis import jackknife


fName = sys.argv[1]
datafile = open(indir + fName, "r")
data = []

for ln in datafile:
    strlist = ln.rsplit(" ")
    strlist = [x for x in strlist if not (x == "\n")]
    try:
        fllist = [float(x) for x in strlist]

        if len(fllist) != 22:
            print("bad line at row " + str(1 + len(data)))
        data.append(fllist)
    except:
        print("bad data at row  " + str(1 + len(data)))
        data.append(strlist)
        load_failed = True

if load_failed:
    exit(-1)
dataMatrix = np.array(data)
ind = np.lexsort(dataMatrix[:, 1], dataMatrix[:, 0])
dataMatrix = dataMatrix[ind]
L_vals, L_inds = np.unique(dataMatrix[:, 0], return_index=True)
N_L = len(L_vals)
L_inds = np.append(L_inds, dataMatrix.shape[0] - 1)

for i in range(len(N_L)):
    L_file = open("./" + repr(dataMatrix[L_inds[i], 0]) + ".avg", "w")
    T_vals, T_inds = np.unique(
        dataMatrix[L_inds[i] : L_inds[i + 1], 1], return_index=True
    )
    N_T = len(T_vals)
    T_inds = np.append(T_inds, L_inds[i + 1])

    for j in range(N_T):
        avgs = []
        deltas = []
        sqrtN_indep = pow(T_inds[j + 1] - T_inds[j], 0.5)
        index_quants = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 21]

        for k in index_quants:
            avgs.append(np.mean(dataMatrix[T_inds[j] : T_inds[j + 1], k]))
            deltas.append(
                np.std(dataMatrix[T_inds[j] : T_inds[j + 1], k]) / sqrtN_indep
            )
