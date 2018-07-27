

x_temp = "T - Temperature"
x_size = "L - Linear System Size"
x_z = "z - Dynamical Critical Exponent"
x_n = r"N\ssweeps\S"
x_omega = r"\xw\0 - First Order Scaling Correction"
x_vstime = "Year"
x_var_nu = x_temp

dict_xaxis = {
    "vsT/omega_fit_var": x_temp,
    "vsT/omega_fit": x_temp,
    "vstime/nu": x_vstime,
    "vstime/eta": x_vstime,
    "twoL/intersection": x_omega,
    "twoL/tc": x_omega,
    "2Lquant_fit/a_bin": x_temp,
    "2Lquant_fit/a_omega_rs": x_temp,
    "2Lquant_fit/omega_bin": x_temp,
    "2Lquant_fit/var_a_bin": x_temp,
    "2Lquant_fit/var_bin": x_temp,
    "2Lquant_fit/var_omega_rs": x_temp,
    "2Lquant_fit/a_omega_bin": x_temp,
    "2Lquant_fit/a_rs": x_temp,
    "2Lquant_fit/omega_rs": x_temp,
    "2Lquant_fit/var_a_rs": x_temp,
    "2Lquant_fit/var_omega_bin": x_temp,
    "2Lquant_fit/var_rs": x_temp,
    "findZ/sigmaVsZ": x_z,
    "subtraction/bin": x_size,
    "subtraction/rs": x_size,
    "threeL/bin": x_temp,
    "threeL/rs": x_temp,
    "twoL/bin": x_temp,
    "twoL/rs": x_temp,
    "vsL/2Lbin": x_size,
    "vsL/2Lrs": x_size,
    "vsL/bin": x_size,
    "vsL/c": x_size,
    "vsL/chi": x_size,
    "vsL/dbdt": x_size,
    "vsL/delta": x_size,
    "vsL/en": x_size,
    "vsL/mag": x_size,
    "vsL/rs": x_size,
    "vsN/teq": x_n,
    "vsO/eta": x_omega,
    "vsO/intersection": x_omega,
    "vsO/nu": x_omega,
    "vsO/tc": x_omega,
    "vsT/bin": x_temp,
    "vsT/c": x_temp,
    "vsT/chi": x_temp,
    "vsT/dbdt": x_temp,
    "vsT/en": x_temp,
    "vsT/eta": x_temp,
    "vsT/mag": x_temp,
    "vsT/nu": x_temp,
    "vsT/rs": x_temp,
    "vsT/var_nu": x_temp,
    "vsT/var_eta": x_temp,
}

y_vstime = r'\xn\0'
y_en = r"e Energy per spin"
y_mag = r"m Magnetization per spin"
y_bin = r"B = \x\ca\0\Cm\S4\N\x\cq\0\C/\x\ca\0\Cm\S2\N\x\cq\0\C\S2\N"
y_bin_sub = r"B(L) - A"
y_rs_sub = r"L\xr\0(L) - A"
y_2Lbin = r"B(2L)-B(L)"
y_2Lrs = r"L\xr\0\ss\N(2L)-L\xr\0\ss\N(L)"
y_dbdt = r"dB/dT"
y_chi = r"\xc\0 Susceptibility"
y_rs = r"L\xr\0\ss\N Superfluid density"
y_m2 = r"m\S2\N"
y_m4 = r"m\S4\N"
y_c = "C - Heat Capacity"
y_teq = "Magnetization"
y_threeL_bin = r"\xw\0 = -ln(B(4L) - B(2L)/B(2L) - B(L))/ln(2)"
y_threeL_rs = r"\xw\0 = -ln(l\xr\0(4L) - l\xr\0(2L)/l\xr\0(2L) - l\xr\0(L))/ln(2)"
y_twoL_bin = r"B(2L) - B(L)"
y_twoL_rs = r"2L\xr\0(2L) - L\x\r\0(L)"
y_vsO = r"\xs\0\sQ(2L)-Q(L)\N"
y_sigmaVsZ = r"\xc\0\S2\N"
y_tc = r"T\sc\S"
y_intersection = r"mean dist to mean point of intersections"
y_eta = r"\xh\0 critical exponent"
y_omega = r"\xw\0"
y_varomega = r"Var(\xw\0)"
y_nu = r"\xn\0 critical exponent"
y_delta = r"CPU hours / N\sMCAvg\S"
y_a_rs = "a from lr(2l) - lr(l) fit"
y_a_bin = "a from bin(2l) - bin(l) fit"
y_omega_rs = r"\xw\0  from  lr(2l) - lr(l) fit"
y_omega_bin = r"\xw\0  from  bin(2l) - bin(l) fit"
y_a_omega_bin = r"\xw\0*a from bin fit"
y_a_omega_rs = r"\xw\0*a from rs fit"
y_var_bin = r"Var(\xw\0) + Var(a) from bin fit"
y_var_rs = r"Var(\xw\0) + Var(a) from rs fit"
y_var_a_rs = r"Var(a)  from  lr(2l) - lr(l) fit"
y_var_a_bin = r"Var(a)  from  bin(2l) - bin(l) fit"
y_var_omega_rs = r"Var(\xw\0)  from  lr(2l) - lr(l) fit"
y_var_omega_bin = r"Var(\xw\0)  from  bin(2l) - bin(l) fit"
y_omega_fit = r"\xw\0 from g(L) fit"
y_omega_fit_var = r"Var(\xw\0) from g(L) fit"
y_var_nu = r'Var(\xn\0) from dB/dT fit'
y_var_eta = r'Var(\xh\0) from \xc\0 fit'

dict_yaxis = {
    "vsT/omega_fit": y_omega_fit,
    "vsT/omega_fit_var": y_omega_fit_var,
    "vsT/var_nu": y_var_nu,
    "vsT/var_eta": y_var_eta,
    "vstime/nu": y_vstime,
    "vstime/eta": y_eta,
    "twoL/intersection": y_intersection,
    "twoL/tc": y_tc,
    "2Lquant_fit/a_bin": y_a_bin,
    "2Lquant_fit/a_omega_rs": y_a_omega_rs,
    "2Lquant_fit/omega_bin": y_omega_bin,
    "2Lquant_fit/var_a_bin": y_var_a_bin,
    "2Lquant_fit/var_bin": y_var_bin,
    "2Lquant_fit/var_omega_rs": y_var_omega_rs,
    "2Lquant_fit/a_omega_bin": y_omega_bin,
    "2Lquant_fit/a_rs": y_a_rs,
    "2Lquant_fit/omega_rs": y_omega_rs,
    "2Lquant_fit/var_a_rs": y_var_a_rs,
    "2Lquant_fit/var_omega_bin": y_var_omega_bin,
    "2Lquant_fit/var_rs": y_var_rs,
    "findZ/sigmaVsZ": y_sigmaVsZ,
    "subtraction/bin": y_bin_sub,
    "subtraction/rs": y_rs_sub,
    "threeL/bin": y_threeL_bin,
    "threeL/rs": y_threeL_rs,
    "twoL/bin": y_twoL_bin,
    "twoL/rs": y_twoL_rs,
    "vsL/2Lbin": y_twoL_bin,
    "vsL/2Lrs": y_twoL_rs,
    "vsL/bin": y_bin,
    "vsL/c": y_c,
    "vsL/chi": y_chi,
    "vsL/dbdt": y_dbdt,
    "vsL/delta": y_delta,
    "vsL/en": y_en,
    "vsL/mag": y_mag,
    "vsL/rs": y_rs,
    "vsN/teq": y_teq,
    "vsO/eta": y_eta,
    "vsO/intersection": y_intersection,
    "vsO/nu": y_nu,
    "vsO/tc": y_tc,
    "vsT/bin": y_bin,
    "vsT/c": y_c,
    "vsT/chi": y_chi,
    "vsT/dbdt": y_dbdt,
    "vsT/en": y_en,
    "vsT/eta": y_eta,
    "vsT/mag": y_mag,
    "vsT/nu": y_nu,
    "vsT/rs": y_rs,
}


dict_log = {
    (True, True): [
        "vsL/2Lbin",
        "vsL/2Lrs",
        "vsL/bin",
        "vsL/c",
        "vsL/chi",
        "vsL/dbdt",
        "vsL/delta",
        "vsL/en",
        "vsL/mag",
        "vsL/rs",
    ],
    (True, False): ["vsN/teq"],
    (False, True): [
        "vsT/omega_fit_var",
        "2Lquant_fit/var_a_bin",
        "2Lquant_fit/var_bin",
        "2Lquant_fit/var_omega_rs",
        "2Lquant_fit/var_a_rs",
        "2Lquant_fit/var_omega_bin",
        "2Lquant_fit/var_rs",
    ],
    (False, False): [
        "vsT/omega_fit",
        "vsT/var_nu",
        "vsT/var_eta",
        "vstime/nu",
        "vstime/eta",
        "twoL/intersection",
        "twoL/tc",
        "vsT/bin",
        "vsT/c",
        "vsT/chi",
        "vsT/dbdt",
        "vsT/en",
        "vsT/eta",
        "vsT/mag",
        "vsT/nu",
        "vsT/rs",
        "vsO/eta",
        "vsO/intersection",
        "vsO/nu",
        "vsO/tc",
        "threeL/bin",
        "threeL/rs",
        "twoL/bin",
        "twoL/rs",
        "2Lquant_fit/a_bin",
        "2Lquant_fit/a_omega_rs",
        "2Lquant_fit/omega_bin",
        "2Lquant_fit/a_omega_bin",
        "2Lquant_fit/a_rs",
        "2Lquant_fit/omega_rs",
        "findZ/sigmaVsZ",
        "subtraction/bin",
        "subtraction/rs",
    ],
}

dict_title = {
    "vsT/omega_fit":"vsT_omega_fit",
    "vsT/omega_fit_var":"vsT_omega_fit_var",
    "vsT/var_eta": "vsT_var_eta",
    "vsT/var_nu": "vsT_var_nu",
    "vstime/eta": "vstime_eta",
    "vstime/nu": "vstime_nu",
    "twoL/intersection": "twoL_intersection",
    "twoL/tc": "twoL_tc",
    "2Lquant_fit/a_bin": "2Lquant_fit_a_bin",
    "2Lquant_fit/a_omega_rs": "2Lquant_fit_a_omega_rs",
    "2Lquant_fit/omega_bin": "2Lquant_fit_omega_bin",
    "2Lquant_fit/var_a_bin": "2Lquant_fit_var_a_bin",
    "2Lquant_fit/var_bin": "2Lquant_fit_var_bin",
    "2Lquant_fit/var_omega_rs": "2Lquant_fit_var_omega_rs",
    "2Lquant_fit/a_omega_bin": "2Lquant_fit_a_omega_bin",
    "2Lquant_fit/a_rs": "2Lquant_fit_a_rs",
    "2Lquant_fit/omega_rs": "2Lquant_fit_omega_rs",
    "2Lquant_fit/var_a_rs": "2Lquant_fit_var_a_rs",
    "2Lquant_fit/var_omega_bin": "2Lquant_fit_var_omega_bin",
    "2Lquant_fit/var_rs": "2Lquant_fit_var_rs",
    "findZ/sigmaVsZ": "findZ_sigmaVsZ",
    "subtraction/bin": "subtraction_bin",
    "subtraction/rs": "subtraction_rs",
    "threeL/bin": "threeL_bin",
    "threeL/rs": "threeL_rs",
    "twoL/bin": "twoL_bin",
    "twoL/rs": "twoL_rs",
    "vsL/2Lbin": "vsL_2Lbin",
    "vsL/2Lrs": "vsL_2Lrs",
    "vsL/bin": "vsL_bin",
    "vsL/c": "vsL_c",
    "vsL/chi": "vsL_chi",
    "vsL/dbdt": "vsL_dbdt",
    "vsL/delta": "vsL_delta",
    "vsL/en": "vsL_en",
    "vsL/mag": "vsL_mag",
    "vsL/rs": "vsL_rs",
    "vsN/teq": "vsN_teq",
    "vsO/eta": "vsO_eta",
    "vsO/intersection": "vsO_intersection",
    "vsO/nu": "vsO_nu",
    "vsO/tc": "vsO_tc",
    "vsT/bin": "vsT_bin",
    "vsT/c": "vsT_c",
    "vsT/chi": "vsT_chi",
    "vsT/dbdt": "vsT_dbdt",
    "vsT/en": "vsT_en",
    "vsT/eta": "vsT_eta",
    "vsT/mag": "vsT_mag",
    "vsT/nu": "vsT_nu",
    "vsT/rs": "vsT_rs",
}
