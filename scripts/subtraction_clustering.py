import numpy as np
import matplotlib.pyplot as plt

import settings
from analysis import intersectionFinder

# results  [ size_index,  a_idx * T_idx, values]
# values  [ a, T, L1, L2, w_b, w_r, dw_b, dw_r ]  0 to 7
results = np.load(settings.pickles_path + '2L_log_omega/results_jul_5_skip_4_128.npy')

NUM_T = np.unique(results[0, :, 1]).shape[0]
NUM_A = np.unique(results[0, :, 0]).shape[0]
NUM_L = results.shape[0]



for a_idx in range(NUM_A):
    intersections = np.empty((NUM_A, NUM_L -1, 4))
    for l_idx in range(NUM_L -1):
        X = results[l_idx, a_idx*NUM_T:(a_idx+1)*NUM_T, 1]
        Y1_b = results[l_idx, a_idx*NUM_T:(a_idx+1)*NUM_T, 4]
        Y2_b = results[l_idx + 1, a_idx*NUM_T:(a_idx+1)*NUM_T, 4]
        Y1_r = results[l_idx, a_idx*NUM_T:(a_idx+1)*NUM_T, 5]
        Y2_r = results[l_idx + 1, a_idx*NUM_T:(a_idx+1)*NUM_T, 5]
        binter = intersectionFinder.findIntersection(X, Y1_b, Y2_b)
        rinter = intersectionFinder.findIntersection(X, Y1_r, Y2_r)
        if len(binter) == 0:
            binter = [np.nan, np.nan]
        else:
            binter = binter[0]
        if len(rinter) == 0:
            rinter = [np.nan, np.nan]
        else:
            rinter = rinter[0]

        intersections[a_idx, l_idx, 0] = binter[0]
        intersections[a_idx, l_idx, 1] = binter[1]
        intersections[a_idx, l_idx, 2] = rinter[0]
        intersections[a_idx, l_idx, 3] = rinter[1]
    bclose = intersectionFinder.findClose_parse(intersections[a_idx, :, :2])
    rclose = intersectionFinder.findClose_parse(intersections[a_idx, :, 2:])
    print(bclose[0], bclose[1], bclose[2], results[0, a_idx*NUM_T, 0], )
    #print(rclose)


