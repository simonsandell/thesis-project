import numpy as np
import settings


def get_bin(mag2, mag4, exp):
    return mag4 * exp / (mag2 * mag2)


def get_rho_s(e, sx, sy, sz, exp, L, T):
    rho_s = -L * e - (L * L * L * L / T) * (sx + sy + sz)
    rho_s = rho_s / (3.0 * exp)

    return rho_s


def calc_omega_func(view1, view2, view3):
    t = view1[0, 1]
    l1 = view1[0, 0]
    l2 = view2[0, 0]
    l3 = view3[0, 0]
    b1 = get_bin(np.mean(view1[:, 10]), np.mean(view1[:, 11]), np.mean(view1[:, 21]))
    b2 = get_bin(np.mean(view2[:, 10]), np.mean(view2[:, 11]), np.mean(view2[:, 21]))
    b3 = get_bin(np.mean(view3[:, 10]), np.mean(view3[:, 11]), np.mean(view3[:, 21]))
    r1 = get_rho_s(
        np.mean(view1[:, 7]),
        np.mean(view1[:, 14]),
        np.mean(view1[:, 15]),
        np.mean(view1[:, 16]),
        np.mean(view1[:, 21]),
        l1,
        t,
    )
    r2 = get_rho_s(
        np.mean(view2[:, 7]),
        np.mean(view2[:, 14]),
        np.mean(view2[:, 15]),
        np.mean(view2[:, 16]),
        np.mean(view2[:, 21]),
        l2,
        t,
    )
    r3 = get_rho_s(
        np.mean(view3[:, 7]),
        np.mean(view3[:, 14]),
        np.mean(view3[:, 15]),
        np.mean(view3[:, 16]),
        np.mean(view3[:, 21]),
        l3,
        t,
    )

    omegabin = -np.log((b3 - b2) / (b2 - b1))
    omegarho = -np.log((r3 - r2) / (r2 - r1))

    return [omegabin, omegarho]


# produce [T, omegabin, omegarho, L1, L2, L3, N1, N2, N3, domegabin, domegarho, ]
def produceResults(arg):
    view1, view2, view3 = arg
    omegabin, omegarho = calc_omega_func(view1, view2, view3)
    jomegas = jackknife.jackknife_3(view1, view2, view3, calc_omega_func, 2, 100)
    t = view1[0, 1]
    l1 = view1[0, 0]
    l2 = view2[0, 0]
    l3 = view3[0, 0]
    n1 = view1.shape[0]
    n2 = view2.shape[0]
    n3 = view3.shape[0]
    domegabin = np.sqrt(jomegas.shape[0] - 1) * np.std(jomegas[:, 0])
    domegarho = np.sqrt(jomegas.shape[0] - 1) * np.std(jomegas[:, 1])

    return [t, omegabin, omegarho, l1, l2, l3, n1, n2, n3, domegabin, domegarho]


def getTviews(mat):
    tv, ti = np.unique(mat[:, 1], return_index=True)
    ti = np.append(ti, mat.shape[0])
    res = []

    for i, (tind1, tind2) in enumerate(zip(ti[:-1], ti[1:])):
        res.append(mat[tind1:tind2, :])
    return res


def threeLmethod(data1, data2, data3, model, savename):
    # datatables for 3 systemsizes
    data1 = data1[data1[:, 1].argsort()]
    data2 = data2[data2[:, 1].argsort()]
    data3 = data3[data3[:, 1].argsort()]
    l1, l2, l3 = data1[0, 0], data2[0, 0], data3[0, 0]
    dat1views = getTviews(data1)
    dat2views = getTviews(data2)
    dat3views = getTviews(data3)
    result = []
    funcargs = []

    for v1, v2, v3 in zip(dat1views, dat2views, dat3views):
        funcargs.append([v1, v2, v3])
    result = pool.map(produceResults, funcargs)
    pool.close()
    pool.join()
    fileWriter.writeThreeLMethod(
        savename + str(l1) + "_" + str(l2) + "_" + str(l3), result
    )

    return result
