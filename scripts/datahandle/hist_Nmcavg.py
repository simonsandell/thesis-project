import numpy as np

def draw_diff_hist(array):
    # take np.array(X , 22)
    # sort by temp, select first T
    array = array[array[:, 1].argsort()]
    tval, idxt = np.unique(array[:, 1],return_index=True)
    array = array[idxt[0]:idxt[1], :]
    # sort by total n mcavg with index: 5
    array = array[array[:, 5].argsort()]
    #compute difference between successors
    diff = np.empty(array.shape[0]-1)
    for i in range(array.shape[0]-1):
        diff[i] = array[i+1, 5] - array[i, 5]
    return diff

def draw_reg_hist(array):
    # take np.array(X , 22)
    # sort by temp, select first T
    array = array[array[:, 1].argsort()]
    tval, idxt = np.unique(array[:, 1],return_index=True)
    array = array[idxt[0]:idxt[1], :]
    # sort by total n mcavg with index: 5
    array = array[array[:, 5].argsort()]
    return array[:,5]
