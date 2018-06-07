def getBin(m2, m4, exp):
    return (m4 * exp) / (m2 * m2)


def getdBdT(M2, M4, M2E, M4E, E, Exp, T, Nspins):
    dbdt = Exp * M4E * M2 + M4 * M2 * E - 2.0 * M4 * M2E * Exp
    dbdt = Nspins * dbdt / (T * T * M2 * M2 * M2)
    return dbdt


def getChi(m, m2, exp, T, Nspins):
    return Nspins * (m2 / exp - m * m / (exp * exp)) / T


def getRs(e, sx, sy, sz, exp, L, T):
    rs = -L * e - (L * L * L * L / T) * (sx + sy + sz)
    rs = rs / (3.0 * exp)
    return rs


def getC(e, e2, exp, T, Nspins):
    c = e2 / exp - e * e / (exp * exp)
    c = c / (T * T)
    c = c * Nspins
    return c
