import os
import numpy as np
from analysis import intersectionFinder


def read_grace_dat(filepath):
    ret = [];
    with open(filepath,"r") as a:
        for line in a:
            if not "#" in line:
                spline = (line.rsplit("    "))
                spline = [x for x in spline if not x==""]
                fline = [float(x) for x in spline[:-1]]
                ret.append(fline)
    return np.array(ret)
pth = "/home/simon/exjobb/modular/foutput/3DXY/vsT/eta/"
pth_var = "/home/simon/exjobb/modular/foutput/3DXY/vsT/var_eta/"
nm = "std_jul_26_final_0.82_skip_2.dat"
nm_var = "std_var_jul_26_final_0.82_skip_2.dat"
var = (read_grace_dat(pth_var + nm_var))
save_var = var.copy()
min_i = np.argmin(var[:, 1])
print(var.shape)
var = var[np.argsort(var[:, 1] )]

val = read_grace_dat(pth + nm)
save_val = val.copy()
val = val[np.argsort(var[:, 1] )]
print(val.shape)

print(np.hstack((var[:,:2],val[:,:])))

omega = save_val[min_i, 1]
domega = save_val[min_i, 2]
tc = save_val[min_i, 0]

cent_diff = (save_val[min_i + 1, 1] - save_val[min_i - 1, 1])/(save_val[min_i + 1, 0] - save_val[min_i - 1, 0])
dtc = domega/cent_diff


var_fdiff = (save_var[min_i + 1, 1] - save_var[min_i, 1])/(save_var[min_i + 1, 0] - save_var[min_i, 0])
var_bdiff = (save_var[min_i, 1] - save_var[min_i - 1, 1])/(save_var[min_i, 0] - save_var[min_i - 1, 0])
m_slope = min([abs(var_fdiff), abs(var_bdiff)])
m_var_delta = max(save_var[min_i-1:min_i+1, 2])

dtc_2 = m_var_delta/m_slope

print('tc', tc, 'delta', dtc, 'delta 2', dtc_2)
print('omega', omega, domega)

max_delta = 2*pow(10,-6)

