import numpy as np
from scipy.optimize import curve_fit
import anaFuncs
import settings
from plotting import fileWriter

#  define some variables, path to datatables
DIRPATH = settings.datatables_path+ "June_26_2018/"
TAG = "jul_5"
JACKPATH = DIRPATH + "/jackknife/"
FILELIST = [
    np.load(settings.DATATABLES[0]),
    np.load(settings.DATATABLES[1]),
    np.load(settings.DATATABLES[2]),
    np.load(settings.DATATABLES[3]),
    np.load(settings.DATATABLES[4]),
    np.load(settings.DATATABLES[5]),
]
JACK_LIST = [
    np.load(settings.JACKTABLES[0]),
    np.load(settings.JACKTABLES[1]),
    np.load(settings.JACKTABLES[2]),
    np.load(settings.JACKTABLES[3]),
    np.load(settings.JACKTABLES[4]),
    np.load(settings.JACKTABLES[5]),
]


def get_temp_idx(arr):
    tval, tidx = np.unique(arr[:, 1], return_index=True)
    tidx2 = tidx.copy()

    for i in range(tidx.shape[0] - 1):
        if np.isclose(arr[tidx[i], 1], arr[tidx[i + 1], 1], rtol=1e-10, atol=1e-10):
            tidx2[i + 1] = 0.0
    tidx = [x for x in tidx2 if not x == 0.0]
    tidx = np.append(tidx, arr.shape[0])
    tidx = np.append(0, tidx)

    return tidx

def calculate_exponents(omega,skip_n):
    if settings.model == "3DXY":
        idx = anaFuncs.get3DXYIndex()
    SAVENAME = TAG + "_" + str(omega) + "_skip_" + str(skip_n)

    def fitfunc(L, nu, a, b):
        res = (L ** (1.0 / nu)) * (a + b * (L ** (-omega)))

        return res

    def etafunc(L, eta, a, b):
        res = (L ** (2 - eta)) * (a + b * (L ** (-omega)))

        return res

    def calculateNu(tview):
        X = tview[:, 0]
        Y = tview[:, idx["DBDT"][0]]
        params, covar = curve_fit(fitfunc, X, Y)
        res = np.empty((1, 4))
        res[0, 0] = tview[0, 1]
        res[0, 1] = params[0]
        res[0, 2] = covar[0, 0]
        res[0, 3] = 0.0

        return res


    def calculateEta(tview):
        X = tview[:, 0]
        Y = tview[:, idx["CHI"][0]]
        params, covar = curve_fit(etafunc, X, Y)
        res = np.empty((1, 4))
        res[0, 0] = tview[0, 1]
        res[0, 1] = params[0]
        res[0, 2] = covar[0, 0]
        res[0, 3] = 0.0

        return res


    # skip first n datatables, then load remaining into all_tables
    filelist = FILELIST[skip_n:]
    jackknife_list = JACK_LIST[skip_n:]
    dt_num_vals = filelist[0].shape[1]
    jack_num_vals = jackknife_list[0].shape[2]
    JACK_NUM = jackknife_list[0].shape[0]
    TEMP_NUM = jackknife_list[0].shape[1]
    L_NUM = len(filelist)
    all_tables = np.empty((0, dt_num_vals))
    jack_tables = np.empty((JACK_NUM, TEMP_NUM,L_NUM, jack_num_vals))

    for dt, jt, l_ind in zip(filelist, jackknife_list, range(len(jackknife_list))):
        all_tables = np.append(all_tables, dt, axis=0)

        # sort all jnum vals in current jt by temp and put in jack_tables
        for j_idx in range(JACK_NUM):
            j_jt = jt[j_idx, :, :];
            j_jt = j_jt[j_jt[:,1].argsort()]
            for t_idx in range(TEMP_NUM):
                jack_tables[j_idx, t_idx, l_ind, :] = j_jt[t_idx, :]

    print("done loading")
    # sort by temperature.
    ind = np.lexsort((all_tables[:, 0], all_tables[:, 1]))
    all_tables = all_tables[ind]
    # temperatures unfortunately not exact, use some isclose magic to group unique temperatures
    # into correct blocks
    Ti = get_temp_idx(all_tables)

    result = np.empty((Ti.shape[0] - 1, 4))
    eta_result = np.empty((Ti.shape[0] - 1, 4))
    # result format : [T exponent var(exponent) N=NL1 + NL2]

    for ind in range(Ti.shape[0] - 1):
        tview = all_tables[Ti[ind] : Ti[ind + 1], :]
        tview = tview[tview[:, 0].argsort()]
        result[ind, :] = calculateNu(tview)
        eta_result[ind, :] = calculateEta(tview)

        jresult = np.empty((0, 4))
        jeta_result = np.empty((0, 4))
        for i in range(JACK_NUM):
            jresult = np.append(jresult, calculateNu(jack_tables[i, ind, :, :]), axis=0)
            jeta_result = np.append(jeta_result, calculateEta(jack_tables[i, ind, :, :]), axis=0)
        nu_delta = pow(JACK_NUM - 1, 0.5) * np.std(jresult[:, 1])
        eta_delta = pow(JACK_NUM - 1, 0.5) * np.std(jeta_result[:, 1])
        result[ind, 2] = nu_delta
        eta_result[ind, 2] = eta_delta


    # write to dat files for plotting
    writePath = settings.foutput_path + settings.model + "/vsT/nu/" + SAVENAME + ".dat"
    eta_Path = settings.foutput_path + settings.model + "/vsT/eta/" + SAVENAME + ".dat"

    fileWriter.writeQuant(writePath, result, [0, 1, 2, 3])
    fileWriter.writeQuant(eta_Path, eta_result, [0, 1, 2, 3])
