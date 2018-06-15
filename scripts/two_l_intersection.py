import numpy as np

from analysis import intersectionFinder
import settings

DATA = [
    np.load(settings.pickles_path + "2Lquant/jun_114_8.npy"),
    np.load(settings.pickles_path + "2Lquant/jun_118_16.npy"),
    np.load(settings.pickles_path + "2Lquant/jun_1116_32.npy"),
    np.load(settings.pickles_path + "2Lquant/jun_1132_64.npy"),
    np.load(settings.pickles_path + "2Lquant/jun_1164_128.npy"),
]
JACK_DATA = [
    np.load(settings.pickles_path + "2Lquant/jackknife/jack_jun_114_8.npy"),
    np.load(settings.pickles_path + "2Lquant/jackknife/jack_jun_118_16.npy"),
    np.load(settings.pickles_path + "2Lquant/jackknife/jack_jun_1116_32.npy"),
    np.load(settings.pickles_path + "2Lquant/jackknife/jack_jun_1132_64.npy"),
    np.load(settings.pickles_path + "2Lquant/jackknife/jack_jun_1164_128.npy"),
] 
NUM_L = len(DATA)
NUM_T = len(DATA[0].shape[0])
NUM_J = len(JACK_DATA[0].shape[0])
# format DATA : l1 l2 t bin rs delbin delrs

for li in range(NUM_L):
    ind = np.lexsort((DATA[li][:,2]))
    DATA[li] = DATA[li][ind]
    for ji in range(NUM_J):
        ind = np.lexsort((JACK_DATA[li][ji,:,2]))
        JACK_DATA[li][ji,:,2] = JACK_DATA[li][ind]

for l_ind_one in range(NUM_L-1):
    for l_ind_two in range(l_ind_one+1,NUM_L):
        for t_ind in range(NUM_T-1):
            X = DATA[l_ind_one][t_ind:(t_ind + 2), 2]
            Y1 = DATA[l_ind_one][t_ind:(t_ind + 2), 3]
            Y2 = DATA[l_ind_two][t_ind:(t_ind + 2), 3]
            reg_int = intersectionFinder.findIntersection(X,Y1,Y2)
            if len(reg_int) > 0:
                break
        all_jack_int = []
        all_jack_int[:] = []
        for j_ind in range(NUM_J):
            for t_ind in range(NUM_T):
                X = JACK_DATA[l_ind_one][t_ind:(t_ind + 2), 2]
                Y1 = JACK_DATA[l_ind_one][t_ind:(t_ind + 2), 3]
                Y2 = JACK_DATA[l_ind_two][t_ind:(t_ind + 2), 3]
                jack_int = intersectionFinder.findIntersection(X,Y1,Y2)

                
