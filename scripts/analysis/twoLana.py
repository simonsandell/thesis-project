import sys
import os
import numpy as np

import settings
from analysis import modelAvgs
from plotting import fileWriter
import anaFuncs


# calculates the L^{w} ( Q(2L) - Q(L)) quantity with omega =0
# for a single temperature
IDX = anaFuncs.get3DXYIndex()


def scalingMethod(view1, view2, model="3DXY"):
    if model == "3DXY":
        result = np.zeros(2)
        bin_1 = view1[IDX["B"][0]]
        bin_2 = view2[IDX["B"][0]]
        rho_1 = view1[IDX["RS"][0]]
        rho_2 = view2[IDX["RS"][0]]
        result[0] = bin_2 - bin_1
        result[1] = rho_2 - rho_1

        return result


def mpfunction(views):
    view1, view2 = views

    if abs(view1[1] - view2[1]) > 0.0000001:
        print(view1[1], view2[1])
        print(view1.shape)
        print(view2.shape)
        sys.exit(1)
    b_res, r_res = scalingMethod(view1, view2)

    return [view1[0], view2[0], view1[1], b_res, r_res]


# take two datatable, jackknife or normal, for 2 L's, calculates a structure containing L^omega(Q[2L] - Q[L])
# format [L1 L2 T bin rho]
def twoLomega(data1, data2):
    # sort by temperature
    ind1 = np.lexsort((data1[:, 4], data1[:, 1]), axis=0)
    ind2 = np.lexsort((data2[:, 4], data2[:, 1]), axis=0)
    data1 = data1[ind1]
    data2 = data2[ind2]

    # check if L2 = 2*L1
    L1 = data1[0, 0]
    L2 = data2[0, 0]
    #print(L1)
    #print(L2)

    if L2 != (2 * L1):
        print(L1)
        print(L2)
        print("not factor 2")
        exit(1)

    # check if same n of temps

    if data1.shape[0] != data2.shape[0]:
        print("not equal number of temps")
        exit(1)
        # 2 L's, one T, 2 results, 2 Nmcavg, 2 deltas = 9
    # result = np.zeros((ti1.shape[0]-1,2+1+2+2+2))
    result = []

    for i in range(data1.shape[0]):
        view1 = data1[i, :]
        view2 = data2[i, :]
        result.append(mpfunction([view1, view2]))
    result = np.array(result)
    result = result[result[:, 2].argsort()]

    return result
