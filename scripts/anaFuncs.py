def dirToXaxis(fullpath):
    if "2Lquant_fit" in fullpath:
        return "T - temperature"
    if "vsT" in fullpath:
        return "T - temperature"

    if "vsL" in fullpath:
        return "L - systemsize"

    if "vsO" in fullpath:
        return "Omega"

    if "vsN" in fullpath:
        return r"N\ssweeps\S"

    if "findZ" in fullpath:
        return "z"

    if "subtraction" in fullpath:
        return "L - systemsize"
    else:
        return "unknown"


def dirToYaxis(dirname):
    dirLex = {
        "en": r"e Energy per spin",
        "mag": r"m Magnetization per spin",
        "bin": r"B = \x\ca\0\Cm\S4\N\x\cq\0\C/\x\ca\0\Cm\S2\N\x\cq\0\C\S2\N",
        "2Lbin": r"B(2L)-B(L)",
        "2Lrs": r"L\xr\0\ss\N(2L)-L\xr\0\ss\N(L)",
        "dbdt": r"dB/dT",
        "chi": r"\xc\0 Susceptibility",
        "rs": r"L\xr\0\ss\N Superfluid density",
        "m2": r"m\S2\N",
        "m4": r"m\S4\N",
        "c": "C - Heat Capacity",
        "teq": "Magnetization",
        "threeL": r"\xw\0 = -ln(Q(4L) - Q(2L)/Q(2L) - Q(L))/ln(2)",
        "twoL": r"L\S\xw\0\N\c7\C[Q(2L) - Q(L)]",
        "vsO": r"\xs\0\sQ(2L)-Q(L)\N",
        "sigmaVsZ": r"\xc\0\S2\N",
        "tc": r"T\sc\S",
        "intersection": r"mean dist to mean point of intersections",
        "eta": r"\xh\0 critical exponent",
        "omega": r"\xw\0",
        "varomega": r"Var(\xw\0)",
        "nu": r"\xn\0 critical exponent",
        "delta": r'CPU hours / N\sMCAvg\S',
        "a_rs": 'a  ---  lr(2l) - lr(l) fit',
        "a_bin": 'a  ---  bin(2l) - bin(l) fit',
        "omega_rs": r'\xw\0  ---  lr(2l) - lr(l) fit',
        "omega_bin": r'\xw\0  ---  bin(2l) - bin(l) fit',
        "a_omega_bin":r'\xw\0*a --- bin fit',
        "a_omega_rs":r'\xw\0*a --- rs fit',
        "var_bin":r'Var(\xw\0) + Var(a) --- bin fit',
        "var_rs":r'Var(\xw\0) + Var(a) --- rs fit',
        "var_a_rs": r'Var(a)  ---  lr(2l) - lr(l) fit',
        "var_a_bin": r'Var(a)  ---  bin(2l) - bin(l) fit',
        "var_omega_rs": r'Var(\xw\0)  ---  lr(2l) - lr(l) fit',
        "var_omega_bin": r'Var(\xw\0)  ---  bin(2l) - bin(l) fit',
    }

    if dirname in dirLex:
        return dirLex[dirname]
    else:
        return "unknown"


def dirToTitle(dirname):
    dirLex = {
        "threeL": "Omega_from_three_L",
        "twoL": "subration_two_L",
        "vsO": "versus_omega",
        "sigmaVsZ": "teq_sigma",
        "tc": "tc",
        "intersection": "intersection",
        "eta": "eta",
        "omega": "omega",
        "varomega": "variace_omega",
        "nu": "nu",
        "delta": 'cputime',
        "2Lbin": "bin_subtraction_2L",
        "2Lrs": "rs_subtraction_2L",
        "en": "Energy",
        "mag": "Magnetization",
        "bin": "BinderCumulant",
        "dbdt": "dBdT",
        "chi": "Susceptibility",
        "rs": "SuperfluidDensity",
        "m2": "M2",
        "m4": "M4",
        "c": "HeatCapacity",
        "omegaBin3L": "omega_from_B",
        "omegaRS3L": "omega_from_rs",
        "omegaBin2L": "Ltoomega_from_B",
        "std_omegaBin2L": "std_intersect_Bin_vs_omega",
        "omegaRS2L": "Ltoomega_from_RS",
        "std_omegaRS2L": "std_intersect_RS_vs_omega",
        "teq": "Equilibration_study",
    }

    if dirname in dirLex:
        return dirLex[dirname]

    return dirname


def dirToLogPlot(fullpath):
    xlog = False
    ylog = False

    if "vsN" in fullpath:
        xlog = True

    if "subtraction" in fullpath:
        xlog = True
        ylog = True

    if "vsL" in fullpath:
        xlog = True
        ylog = True 
    if "var_" in fullpath:
        ylog = True

    return [xlog, ylog]


def getParams(dirname, fullpath, doPrint):
    title = dirToTitle(dirname)
    xaxis = dirToXaxis(fullpath)
    yaxis = dirToYaxis(dirname)
    [xlog, ylog] = dirToLogPlot(fullpath)

    return [fullpath, title, xaxis, yaxis, xlog, ylog, doPrint]


# datatable indices, boldface quants are good
# add "last" to get delta
def get3DXYIndex():
    res = {
        "L": 0,
        "T": 1,
        "eqsw": 2,
        "eqcl": 3,
        "totsw": 4,
        "totcl": 5,
        "cold": 6,
        "e": 7,
        "e2": 8,
        "m": 9,
        "m2": 10,
        "m4": 11,
        "m2e": 12,
        "m4e": 13,
        "s2x": 14,
        "s2y": 15,
        "s2z": 16,
        "b": [17, "bin"],
        "dbdt": [18, "dbdt"],
        "chi": [19, "chi"],
        "rs": [20, "rs"],
        "expF": 21,
        "B": [22, "bin"],
        "C": [23, "c"],
        "CHI": [24, "chi"],
        "DBDT": [25, "dbdt"],
        "RS": [26, "rs"],
        "EN": [27, "en"],
        "MAG": [28, "mag"],
        "Nmcavg": 29,
        "last": 30,
    }

    return res
