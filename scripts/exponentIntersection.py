import numpy as np
from scipy.optimize import curve_fit
from plotting import fileWriter
from analysis import intersectionFinder
import anaFuncs
import settings

TAG = "jun_28"

DIRPATH = settings.datatables_path + "June_26_2018/"
FILELIST = [
    np.load(DIRPATH + "datatable_4.0jun_153DXY.npy"),
    np.load(DIRPATH + "datatable_8.0jun_153DXY.npy"),
    np.load(DIRPATH + "datatable_16.0jun_153DXY.npy"),
    np.load(DIRPATH + "datatable_32.0jun_263DXY.npy"),
    np.load(DIRPATH + "datatable_64.0jun_263DXY.npy"),
    np.load(DIRPATH + "datatable_128.0jun_263DXY.npy"),
]
JACKLIST = [
    np.load(DIRPATH + "jackknife/4combined_nf.npy"),
    np.load(DIRPATH + "jackknife/8combined_nf.npy"),
    np.load(DIRPATH + "jackknife/16combined_nf.npy"),
    np.load(DIRPATH + "jackknife/32combined_nf.npy"),
    np.load(DIRPATH + "jackknife/64combined_nf.npy"),
    np.load(DIRPATH + "jackknife/128combined_nf.npy"),
]

JACK_NUM = JACKLIST[0].shape[0]
TEMP_NUM = JACKLIST[0].shape[1]
print('JACK_NUM', JACK_NUM)
print('TEMP_NUM', TEMP_NUM)
idx = anaFuncs.get3DXYIndex()

def calc_exponents(omega, skip_n):
    def fitfunc(L, nu, a, b):
        res = pow(L, (1.0 / nu)) * (a + b * (L ** (-omega)))

        return res

    def etafunc(L, eta, a, b):
        res = pow(L, (2 - eta)) * (a + b * (L ** (-omega)))

        return res

    def calc_nu(tview):
        x = tview[:, 0]
        y = tview[:, idx["DBDT"][0]]
        params, covar = curve_fit(fitfunc, x, y)
        res = np.empty((1, 4))
        res[0, 0] = tview[0, 1]
        res[0, 1] = params[0]
        res[0, 2] = covar[0, 0]

        return res

    def calc_eta(tview):
        x = tview[:, 0]
        y = tview[:, idx["CHI"][0]]
        params, covar = curve_fit(etafunc, x, y)
        res = np.empty((1, 4))
        res[0, 0] = tview[0, 1]
        res[0, 1] = params[0]
        res[0, 2] = covar[0, 0]

        return res

    filelist = FILELIST[skip_n:]
    jacklist = JACKLIST[skip_n:]
    quant_num = filelist[0].shape[1]
    jquant_num = jacklist[0].shape[2]
    size_num = len(filelist)
    
    all_data = np.empty((size_num, TEMP_NUM, quant_num))
    all_jdata = np.empty((JACK_NUM, size_num, TEMP_NUM, jquant_num))

    for s_idx in range(size_num):
        sorted_data = filelist[s_idx][filelist[s_idx][:, 1].argsort()]
        all_data[s_idx, :, :] = sorted_data
        for j_idx in range(JACK_NUM):
            uniJ = jacklist[s_idx][j_idx, :, :]
            sorted_data = uniJ[uniJ[:, 1].argsort()]
            all_jdata[j_idx, s_idx, :, :] = sorted_data


    result = np.empty((TEMP_NUM, 4))
    eta_result = np.empty((TEMP_NUM, 4))
    jack_nu_res = np.empty((JACK_NUM, TEMP_NUM, 4))
    jack_eta_res = np.empty((JACK_NUM, TEMP_NUM, 4))
    # result format : T nu deltanu N

    for ind in range(TEMP_NUM):
        # pick out range of values vs L for specific t...
        tview = all_data[:, ind, :]
        # sort by L
        tview = tview[tview[:, 0].argsort()] 
        # fit to functions
        result[ind, :] = calc_nu(tview)
        eta_result[ind, :] = calc_eta(tview)

        for jack_n in range(JACK_NUM):
            jack_nu_res[jack_n, ind, :] = calc_nu(all_jdata[jack_n, :, ind, :])
            jack_eta_res[jack_n, ind, :] = calc_eta(all_jdata[jack_n, :, ind, :])

    return [result, eta_result, jack_nu_res, jack_eta_res]


# for a range of omegas, find different nu,eta curves by curve_fit by succesively omitting smallest L points
# for each omega, find the intersection points of those nu/eta-curves and check their closeness/clustering.
ORANGE = np.linspace(0.5, 1.5, 50)
N_SKIP_RANGE = [0, 1, 2, 3]
nu_close = np.empty((ORANGE.shape[0], 7))
eta_close = np.empty((ORANGE.shape[0], 7))

for index, o in enumerate(ORANGE):
    nu_curves = np.empty((len(N_SKIP_RANGE), 101, 4))
    eta_curves = np.empty((len(N_SKIP_RANGE), 101, 4))
    jack_nu_curves = np.empty((JACK_NUM, len(N_SKIP_RANGE), 101, 4))
    jack_eta_curves = np.empty((JACK_NUM, len(N_SKIP_RANGE), 101, 4))

    for n in N_SKIP_RANGE:
        nu_curves[n, :, :], eta_curves[n, :, :], jack_nu_curves[
            :, n, :, :
        ], jack_eta_curves[:, n, :, :] = calc_exponents(o, n)
    # for all pairs of curves, find intersections
    # try only consecutive curves maybe
    nu_ints = []
    eta_ints = []
    jack_nu_ints = []
    jack_eta_ints = []
    X = nu_curves[0, :, 0]

    for i in range(len(N_SKIP_RANGE) - 1):
        Y1 = nu_curves[i, :, 1]
        Y2 = nu_curves[i+1, :, 1]
        tmpint = intersectionFinder.findIntersection(X, Y1, Y2)

        if tmpint.shape[0] != 0:
            nu_ints.append(tmpint)
        temp_jack_cont = []
        temp_jack_cont[:] = []

        for j_num in range(JACK_NUM):
            Y1 = jack_nu_curves[j_num, i, :, 1]
            Y2 = jack_nu_curves[j_num, i+1, :, 1]
            tmpint = intersectionFinder.findIntersection(X, Y1, Y2)
            temp_jack_cont.append(tmpint)
        jack_nu_ints.append(temp_jack_cont)

        Y1 = eta_curves[i, :, 1]
        Y2 = eta_curves[i+1, :, 1]
        tmpint = intersectionFinder.findIntersection(X, Y1, Y2)

        if tmpint.shape[0] != 0:
            eta_ints.append(tmpint)
        temp_jack_cont = []
        temp_jack_cont[:] = []

        for j_num in range(JACK_NUM):
            Y1 = jack_eta_curves[j_num, i, :, 1]
            Y2 = jack_eta_curves[j_num, i+1, :, 1]
            tmpint = intersectionFinder.findIntersection(X, Y1, Y2)
            temp_jack_cont.append(tmpint)
        jack_eta_ints.append(temp_jack_cont)
    # calculate how close the intersectionpoints are
    print("nu_ints")
    print(len(nu_ints))
    print("eta_ints")
    print(len(eta_ints))
    nu_cl, avgTnu, avgNu = intersectionFinder.findCloseness(nu_ints)
    eta_cl, avgTeta, avgEta = intersectionFinder.findCloseness(eta_ints)

    ls_j_nu_cl = []
    ls_j_eta_cl = []
    ls_j_avgTnu = []
    ls_j_avgTeta = []
    ls_j_avgNu = []
    ls_j_avgEta = []

    ls_j_nu_cl[:] = []
    ls_j_eta_cl[:] = []
    ls_j_avgTnu[:] = []
    ls_j_avgTeta[:] = []
    ls_j_avgNu[:] = []
    ls_j_avgEta[:] = []

    for j_num in range(JACK_NUM):
        jack_nu_cl, jack_avgTnu, jack_avgNu = intersectionFinder.findCloseness(nu_ints)
        jack_eta_cl, jack_avgTeta, jack_avgEta = intersectionFinder.findCloseness(
            eta_ints
        )
        ls_j_nu_cl.append(jack_nu_cl)
        ls_j_eta_cl.append(jack_eta_cl)
        ls_j_avgTnu.append(jack_avgTnu)
        ls_j_avgTeta.append(jack_avgTeta)
        ls_j_avgNu.append(jack_avgNu)
        ls_j_avgEta.append(jack_avgEta)

    # save as [omega closeness avgNu/eta, avgTc]
    print([o, nu_cl, avgNu, avgTnu])
    nu_close[index, :] = [
        o,
        nu_cl,
        avgNu,
        avgTnu,
        pow(JACK_NUM - 1, 0.5) * np.std(ls_j_nu_cl),
        pow(JACK_NUM - 1, 0.5) * np.std(ls_j_avgNu),
        pow(JACK_NUM - 1, 0.5) * np.std(ls_j_avgTnu),
    ]

    eta_close[index, :] = [
        o,
        eta_cl,
        avgEta,
        avgTeta,
        pow(JACK_NUM - 1, 0.5) * np.std(ls_j_eta_cl),
        pow(JACK_NUM - 1, 0.5) * np.std(ls_j_avgEta),
        pow(JACK_NUM - 1, 0.5) * np.std(ls_j_avgTeta),
    ]

# write three plots, closeness vs omega, exponent vs omega, Tc vs omega
close_path = settings.foutput_path + settings.model + "/vsO/intersection/" + TAG
eta_path = (
    settings.foutput_path + settings.model + "/vsO/eta/" + TAG + "eta_vs_omega.dat"
)
nu_path = settings.foutput_path + settings.model + "/vsO/nu/" + TAG + "nu_vs_omega.dat"
tc_path = settings.foutput_path + settings.model + "/vsO/tc/" + TAG + "tc_from_"
fileWriter.writeQuant(close_path + "closeness_nu.dat", nu_close, [0, 1, 4])
# closeness_nu vs omega
fileWriter.writeQuant(close_path + "closeness_eta.dat", eta_close, [0, 1, 4])
# closeness_eta vs omega
fileWriter.writeQuant(nu_path, nu_close, [0, 2, 5])
fileWriter.writeQuant(eta_path, eta_close, [0, 2, 5])
fileWriter.writeQuant(tc_path + "nu.dat", nu_close, [0, 3, 6])
fileWriter.writeQuant(tc_path + "eta.dat", eta_close, [0, 3, 6])
