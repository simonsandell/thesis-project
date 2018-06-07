import numpy as np
import anaFuncs
import settings
import sys
from scipy.optimize import curve_fit
from plotting import fileWriter
from analysis import intersectionFinder


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
        res[0, 3] = np.sum(tview[:, 29])
        return res

    def calculateEta(tview):
        X = tview[:, 0]
        Y = tview[:, idx["CHI"][0]]
        params, covar = curve_fit(etafunc, X, Y)
        res = np.empty((1, 4))
        res[0, 0] = tview[0, 1]
        res[0, 1] = params[0]
        res[0, 2] = covar[0, 0]
        res[0, 3] = np.sum(tview[:, 29])
        return res

    dirpath = settings.root_path + "modular/datatables/combined/"
    savename = "combined_omega_" + str(omega) + "_skip_" + str(skip_n)
    filelist = [
        dirpath + "datatable_4combined3DXY.npy",
        dirpath + "datatable_8combined3DXY.npy",
        dirpath + "datatable_16combined3DXY.npy",
        dirpath + "datatable_32combined3DXY.npy",
        dirpath + "datatable_64combined3DXY.npy",
        dirpath + "datatable_128combined3DXY.npy",
    ]
    filelist = filelist[skip_n:]
    asdf = np.load(filelist[0])
    shape = asdf.shape[1]
    all_tables = np.empty((0, shape))
    for f in filelist:
        dt = np.load(f)
        all_tables = np.append(all_tables, dt, axis=0)

    ind = np.lexsort((all_tables[:, 0], all_tables[:, 1]))
    all_tables = all_tables[ind]
    Tv, Ti = np.unique(all_tables[:, 1], return_index=True)
    Ti2 = Ti.copy()
    for i in range(Ti.shape[0] - 1):
        if np.isclose(
            all_tables[Ti[i], 1], all_tables[Ti[i + 1], 1], rtol=1e-10, atol=1e-10
        ):
            Ti2[i + 1] = 0.0
    Ti = [x for x in Ti2 if not x == 0.0]
    Ti = np.append(Ti, all_tables.shape[0])
    Ti = np.append(0, Ti)
    idx = anaFuncs.get3DXYIndex()
    result = np.empty((Ti.shape[0] - 1, 4))
    eta_result = np.empty((Ti.shape[0] - 1, 4))
    # result format : T nu deltanu N
    for ind in range(Ti.shape[0] - 1):
        tview = all_tables[Ti[ind] : Ti[ind + 1], :]
        tview = tview[tview[:, 0].argsort()]
        result[ind, :] = calculateNu(tview)
        eta_result[ind, :] = calculateEta(tview)
    return [result, eta_result]


# for a range of omegas, find different nu,eta curves by curve_fit by succesively omitting smallest L points
# for each omega, find the intersection points of those nu/eta-curves and check their closeness/clustering.
orange = np.linspace(0.5, 1.0, 30)
nrange = [0, 1, 2, 3]
nu_close = np.empty((orange.shape[0], 4))
eta_close = np.empty((orange.shape[0], 4))
for index, o in enumerate(orange):
    nu_curves = np.empty((len(nrange), 101, 4))
    eta_curves = np.empty((len(nrange), 101, 4))
    for n in nrange:
        nu_curves[n, :, :], eta_curves[n, :, :] = calculateExponents(o, n)
    # for all pairs of curves, find intersections
    nu_ints = []
    eta_ints = []
    X = nu_curves[0, :, 0]
    for i in range(len(nrange) - 1):
        for j in range(i + 1, len(nrange) - 1):
            Y1 = nu_curves[i, :, 1]
            Y2 = nu_curves[j, :, 1]
            tmpint = intersectionFinder.findIntersection(X, Y1, Y2)
            if tmpint.shape[0] != 0:
                nu_ints.append(tmpint)
            Y1 = eta_curves[i, :, 1]
            Y2 = eta_curves[j, :, 1]
            tmpint = intersectionFinder.findIntersection(X, Y1, Y2)
            if tmpint.shape[0] != 0:
                eta_ints.append(tmpint)
    # calculate how close the intersectionpoints are
    nu_cl, avgTnu, avgNu = intersectionFinder.findCloseness(nu_ints)
    eta_cl, avgTeta, avgEta = intersectionFinder.findCloseness(eta_ints)
    # save as [omega closeness avgNu/eta, avgTc]
    print([o, nu_cl, avgNu, avgTnu])
    nu_close[index, :] = [o, nu_cl, avgNu, avgTnu]
    eta_close[index, :] = [o, eta_cl, avgEta, avgTeta]

# write three plots, closeness vs omega, exponent vs omega, Tc vs omega
close_path = settings.foutput_path + settings.model + "/vsO/intersection/"
eta_path = settings.foutput_path + settings.model + "/vsO/eta/eta_vs_omega.dat"
nu_path = settings.foutput_path + settings.model + "/vsO/nu/nu_vs_omega.dat"
tc_path = settings.foutput_path + settings.model + "/vsO/tc/tc_from_"
fileWriter.writeQuantNoDY(close_path + "closeness_nu.dat", nu_close, [0, 1])
# closeness_nu vs omega
fileWriter.writeQuantNoDY(close_path + "closeness_eta.dat", eta_close, [0, 1])
# closeness_eta vs omega
fileWriter.writeQuantNoDY(nu_path, nu_close, [0, 2])
fileWriter.writeQuantNoDY(eta_path, eta_close, [0, 2])
fileWriter.writeQuantNoDY(tc_path + "nu.dat", nu_close, [0, 3])
fileWriter.writeQuantNoDY(tc_path + "eta.dat", eta_close, [0, 3])
