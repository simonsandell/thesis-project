import numpy as np

import settings
import subtractionMethod
from analysis import intersectionFinder

# results  [ size_index,  a_idx * T_idx, values]
# values  [ a, T, L1, L2, w_b, w_r, dw_b, dw_r ]  0 to 7
brow = 0.0
a_last = 0.0
a_new= 1.0
TOL = 10e-10
amin =  1.2415
amax =  1.246
while abs(a_last-a_new) > TOL:
    nametag = 'u4_skip_4_128'
    a_last = a_new
    subtractionMethod.subtract_A_between(amin, amax, "temporary",[0,5])
    results = np.load(settings.pickles_path + '2L_log_omega/results_temporary.npy')
    NUM_T = np.unique(results[0, :, 1]).shape[0]
    NUM_A = np.unique(results[0, :, 0]).shape[0]
    NUM_L = results.shape[0]
    bclose = np.empty((0,4))
    rclose = np.empty((0,4))
    
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
        btemp = np.empty((1,4))
        btemp[0,:3]=  np.array(intersectionFinder.findClose_parse(intersections[a_idx, :, :2]))
        btemp[0, 3] = results[0, a_idx*NUM_T, 0]
        bclose = np.append(bclose, btemp, axis=0)
    abest_idx = bclose[:, 0].argmin()
    brow = bclose[abest_idx, :]
    a_new = brow[2]
    amin = bclose[abest_idx-1, 3]
    print(brow)
    print(bclose)
    print(abest_idx)
    amax = bclose[abest_idx + 1, 3]
#np.save(settings.pickles_path + "2L_log_omega/"+nametag,results)

    
