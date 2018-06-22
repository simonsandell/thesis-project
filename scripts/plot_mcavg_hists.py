import os
import sys
import numpy as np
import matplotlib.pyplot as plt

import settings
from datahandle import textToFloats
from datahandle import hist_Nmcavg

def print_mean_diff(arr, per):
    dif = []
    k = 0
    per = int(per)
    while True:
        try:
            dif.append( arr[k+per] - arr[k])
            k+= 1
        except:
            break
    print(np.mean(dif))
    input()




def draw_hist(arr,titel):
    plt.title(titel)
    plt.plot(arr,'rx')
    plt.show()

TARGET_DIR = sys.argv[1]
NVALS = 22

RESULT = []
FILENAMES = sorted(os.listdir(TARGET_DIR))
NUM_FILES = len(FILENAMES)

for filename in FILENAMES:
    if os.path.isfile(os.path.join(TARGET_DIR, filename)):
        ret = textToFloats.loadData(os.path.join(TARGET_DIR, filename), NVALS)
        ret = np.array(ret)
        diffs = hist_Nmcavg.draw_reg_hist(ret)
        print(diffs.shape)
        print(filename)
        draw_hist(diffs, filename)
        period = input("period: ")
        print_mean_diff(diffs, period);


