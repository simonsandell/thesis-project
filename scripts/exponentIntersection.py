import numpy as np
from scipy.optimize import curve_fit
from plotting import fileWriter
from analysis import intersectionFinder
import anaFuncs
import settings

TAG = "jun_11"
JACK_NUM = 100;
TEMP_NUM = 101;

dirpath = settings.datatables_path + "June_11_2018/"
FILELIST= [
        np.load(dirpath + "datatable_4.0jun113DXY.npy"),
        np.load(dirpath + "datatable_8.0jun113DXY.npy"),
        np.load(dirpath + "datatable_16.0jun113DXY.npy"),
        np.load(dirpath + "datatable_32.0jun113DXY.npy"),
        np.load(dirpath + "datatable_64.0jun113DXY.npy"),
        np.load(dirpath + "datatable_128.0jun113DXY.npy"),
    ]
JACKLIST= [
        np.load(dirpath + "jackknife/4combined.npy"),
        np.load(dirpath + "jackknife/8combined.npy"),
        np.load(dirpath + "jackknife/16combined.npy"),
        np.load(dirpath + "jackknife/32combined.npy"),
        np.load(dirpath + "jackknife/64combined.npy"),
        np.load(dirpath + "jackknife/128combined.npy"),
]
def calculateExponents(omega, skip_n):
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
        return res

    def calculateEta(tview):
        X = tview[:, 0]
        Y = tview[:, idx["CHI"][0]]
        params, covar = curve_fit(etafunc, X, Y)
        res = np.empty((1, 4))
        res[0, 0] = tview[0, 1]
        res[0, 1] = params[0]
        res[0, 2] = covar[0, 0]
        return res

    filelist = FILELIST[skip_n:]
    jacklist = JACKLIST[skip_n:]
    savename = TAG + "_" + str(omega) + "_skip_" + str(skip_n)
    shape = filelist[0].shape[1]
    jshape = jacklist[0].shape[1]
    all_tables = np.empty((0, shape))
    all_jacks = np.empty((JACK_NUM,len(filelist),TEMP_NUM, jshape))
    for dt in filelist:
        all_tables = np.append(all_tables, dt, axis=0)
    for l_num,jt in enumerate(jacklist):
        t_sort = jt[jt[:,1].argsort()]
        for jack_n in range(JACK_NUM):
            all_jacks[jack_n,l_num,:,:] = t_sort[jack_n::JACK_NUM,:]

    ind = np.lexsort((all_tables[:, 0], all_tables[:, 1]))
    all_tables = all_tables[ind]
    Tv, Ti = np.unique(all_tables[:, 1], return_index=True)
    Ti2 = Ti.copy()
    for tind in range(Ti.shape[0] - 1):
        if np.isclose(
                all_tables[Ti[tind], 1], all_tables[Ti[tind + 1], 1], rtol=1e-10, atol=1e-10
        ):
            Ti2[tind + 1] = 0.0
    Ti = [x for x in Ti2 if not x == 0.0]
    Ti = np.append(Ti, all_tables.shape[0])
    Ti = np.append(0, Ti)
    idx = anaFuncs.get3DXYIndex()
    result = np.empty((Ti.shape[0] - 1, 4))
    eta_result = np.empty((Ti.shape[0] - 1, 4))
    jack_nu_res = np.empty((JACK_NUM, Ti.shape[0] - 1, 4))
    jack_eta_res = np.empty((JACK_NUM, Ti.shape[0] - 1, 4))
    # result format : T nu deltanu N
    for ind in range(Ti.shape[0] - 1):
        tview = all_tables[Ti[ind] : Ti[ind + 1], :]
        tview = tview[tview[:, 0].argsort()]
        result[ind, :] = calculateNu(tview)
        eta_result[ind, :] = calculateEta(tview)
        for jack_n in range(JACK_NUM):
            jack_nu_res[jack_n,ind,:] = calculateNu(all_jacks[jack_n,:,ind,:])
            jack_eta_res[jack_n,ind,:] = calculateEta(all_jacks[jack_n,:,ind,:])

    return [result, eta_result, jack_nu_res, jack_eta_res]


# for a range of omegas, find different nu,eta curves by curve_fit by succesively omitting smallest L points
# for each omega, find the intersection points of those nu/eta-curves and check their closeness/clustering.
ORANGE = np.linspace(0.5, 1.0, 30)
N_SKIP_RANGE = [0, 1, 2, 3]
nu_close = np.empty((ORANGE.shape[0], 7))
eta_close = np.empty((ORANGE.shape[0], 7))
for index, o in enumerate(ORANGE):
    nu_curves = np.empty((len(N_SKIP_RANGE), 101, 4))
    eta_curves = np.empty((len(N_SKIP_RANGE), 101, 4))
    jack_nu_curves = np.empty((JACK_NUM, len(N_SKIP_RANGE), 101, 4))
    jack_eta_curves = np.empty((JACK_NUM, len(N_SKIP_RANGE), 101, 4))
    for n in N_SKIP_RANGE:
        nu_curves[n, :, :], eta_curves[n, :, :], jack_nu_curves[:, n, :, :], jack_eta_curves[:, n, :, :] = calculateExponents(o, n)
    # for all pairs of curves, find intersections
    # try only consecutive curves maybe
    nu_ints = []
    eta_ints = []
    jack_nu_ints = []
    jack_eta_ints = []
    X = nu_curves[0, :, 0]
    for i in range(len(N_SKIP_RANGE) - 1):
        for j in range(i + 1, len(N_SKIP_RANGE)):
            Y1 = nu_curves[i, :, 1]
            Y2 = nu_curves[j, :, 1]
            tmpint = intersectionFinder.findIntersection(X, Y1, Y2)
            if tmpint.shape[0] != 0:
                nu_ints.append(tmpint)
            temp_jack_cont = []
            temp_jack_cont[:] = []
            for j_num in range(JACK_NUM):
                Y1 = jack_nu_curves[j_num,i,:,1]
                Y2 = jack_nu_curves[j_num,j,:,1]
                tmpint = intersectionFinder.findIntersection(X,Y1,Y2)
                temp_jack_cont.append(tmpint)
            jack_nu_ints.append(temp_jack_cont)


            Y1 = eta_curves[i, :, 1]
            Y2 = eta_curves[j, :, 1]
            tmpint = intersectionFinder.findIntersection(X, Y1, Y2)
            if tmpint.shape[0] != 0:
                eta_ints.append(tmpint)
            temp_jack_cont = []
            temp_jack_cont[:] = []
            for j_num in range(JACK_NUM):
                Y1 = jack_eta_curves[j_num,i,:,1]
                Y2 = jack_eta_curves[j_num,j,:,1]
                tmpint = intersectionFinder.findIntersection(X,Y1,Y2)
                temp_jack_cont.append(tmpint)
            jack_eta_ints.append(temp_jack_cont)
    # calculate how close the intersectionpoints are
    print("nu_ints")
    print(len(nu_ints))
    print("eta_ints")
    print(len(eta_ints))
    nu_cl, avgTnu, avgNu = intersectionFinder.findCloseness(nu_ints)
    eta_cl, avgTeta, avgEta = intersectionFinder.findCloseness(eta_ints)

    ls_j_nu_cl = [];
    ls_j_eta_cl = [];
    ls_j_avgTnu = [];
    ls_j_avgTeta = [];
    ls_j_avgNu = [];
    ls_j_avgEta = [];
    for j_num in range(JACK_NUM):
        jack_nu_cl, jack_avgTnu, jack_avgNu = intersectionFinder.findCloseness(nu_ints)
        jack_eta_cl, jack_avgTeta, jack_avgEta = intersectionFinder.findCloseness(eta_ints)
        ls_j_nu_cl.append(jack_nu_cl)
        ls_j_eta_cl.append(jack_eta_cl)
        ls_j_avgTnu.append(jack_avgTnu)
        ls_j_avgTeta.append(jack_avgTeta)
        ls_j_avgNu.append(jack_avgNu)
        ls_j_avgEta.append(jack_avgEta)

    # save as [omega closeness avgNu/eta, avgTc]
    print([o, nu_cl, avgNu, avgTnu])
    nu_close[index, :] = [o, nu_cl, avgNu, avgTnu,
            pow(JACK_NUM -1,0.5)*np.std(ls_j_nu_cl),
            pow(JACK_NUM -1,0.5)*np.std(ls_j_avgNu),
            pow(JACK_NUM -1,0.5)*np.std(ls_j_avgTnu),
            ]

    eta_close[index, :] = [o, eta_cl, avgEta, avgTeta,
            pow(JACK_NUM -1,0.5)*np.std(ls_j_eta_cl),
            pow(JACK_NUM -1,0.5)*np.std(ls_j_avgEta),
            pow(JACK_NUM -1,0.5)*np.std(ls_j_avgTeta),
            ]

# write three plots, closeness vs omega, exponent vs omega, Tc vs omega
close_path = settings.foutput_path + settings.model + "/vsO/intersection/" + TAG  
eta_path = settings.foutput_path + settings.model + "/vsO/eta/" + TAG + "eta_vs_omega.dat"
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
