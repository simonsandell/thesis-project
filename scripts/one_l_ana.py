from multiprocessing import Pool
import os
import math
import sys
import datetime
import numpy as np

import settings
from plotting import fileWriter
from plotting import datatableToPlots
from analysis import modelAvgs as ma, jackknife

if __name__ == "__main__":
    FILEPATH = sys.argv[1]
    TAG = sys.argv[2]
    MODEL = settings.model
    #data = pickler.loadData(model+FILEPATH)
    DATA = np.load(FILEPATH)
    #sort data
    IND = np.lexsort((DATA[:, 1], DATA[:, 0]))
    DATA = DATA[IND]
    def model_avgs(avgs, mod=MODEL):
        ma_res = np.zeros(7)
        if mod == "3DXY":
            ma_res[0] = ma.getBin(avgs[10], avgs[11], avgs[21])
            ma_res[1] = ma.getC(avgs[7], avgs[8], avgs[21], avgs[1], math.pow(avgs[0], 3))
            ma_res[2] = ma.getChi(avgs[9], avgs[10], avgs[21], avgs[1], math.pow(avgs[0], 3))
            ma_res[3] = ma.getdBdT(avgs[10], avgs[11], avgs[12], avgs[13],
                                   avgs[7], avgs[21], avgs[1], math.pow(avgs[0], 3))
            ma_res[4] = ma.getRs(avgs[7], avgs[14], avgs[15], avgs[16], avgs[21], avgs[0], avgs[1])
            ma_res[5] = avgs[7]/avgs[21]
            ma_res[6] = avgs[9]/avgs[21]
        return ma_res
    #calculate average of all columns, pass that to modelAvgs to obtain bin, dbdt, chi etc
    #return nparray [avg(columns), modelAvgs(avgs)]
    def avg_f(arr):
        f_res = np.zeros(arr.shape[1])
        for i in range(arr.shape[1]):
            f_res[i] = (np.mean(arr[:, i]))
        modavgs = model_avgs(f_res)
        f_res = np.append(f_res, modavgs)
        return f_res
    #for a block with one T value
    def one_l_one_t(view):
        avg = avg_f(view)
        j_est = jackknife.jackknife(view, avg_f, avg.shape[0])
        current_t = repr(view[0, 1])
        current_l = repr(view[0, 0])
        np.save(settings.datatables_path+"jackknife/j_est_" + current_l+"_"+current_t, j_est)
        j_std = np.std(j_est, axis=0)
        avg = np.append(avg, view.shape[0])# add number of mcavgs to result
        j_delta = j_std*np.sqrt(j_est.shape[0]-1)
        avg = np.append(avg, j_delta)
        return avg
    # find indices
    ARGS = []
    LV, LI = np.unique(DATA[:, 0], return_index=True)
    if not len(LV) == 1:
        print(LV)
        sys.exit(1)
    TV, TI = np.unique(DATA[:, 1], return_index=True)
    print(TV)
    print(len(TV))
    if not len(TV) == 101:
        sys.exit(101)
    TI = np.append(TI, DATA.shape[0])
    for t1, t2 in zip(TI[:-1], TI[1:]):
        ARGS.append(DATA[t1:t2, :])
    print("number of jobs: " + str(len(ARGS)))
    RES = []
    NPROC = settings.nprocs
    print("nproc="+str(NPROC))
    POOL = Pool(processes=NPROC, maxtasksperchild=1)
    RES.append(POOL.map(one_l_one_t, ARGS))
    POOL.close()
    POOL.join()
    RES = np.array(RES)
    RES = RES.squeeze()
    # save text file for visual inspeciton
    fileWriter.writeDataTable(TAG, RES)
    # save npy file for further analysis
    FOLDERNAME = datetime.date.today().strftime("%B_%d_%Y")

    if not os.path.exists(settings.datatables_path+FOLDERNAME):
        os.makedirs(settings.datatables_path+FOLDERNAME)
    np.save(settings.datatables_path+"/datatable_"+repr(LV[0])+TAG+MODEL, RES)
    # make plots from  the npy datatables
    datatableToPlots.datatableToPlots(settings.datatables_path+FOLDERNAME, TAG)
