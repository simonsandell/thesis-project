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
pth = "/home/simon/exjobb/modular/foutput/3DXY/2Lquant_fit/omega_bin/"
a = (read_grace_dat(pth + "/asdf.dat"))
b = (read_grace_dat(pth+"/2jul_26_final_skip_.dat"))
print(a.shape, b.shape)
x = a[:, 0]
y1 = a[:, 1]
y2 = b[:, 1]
dy1 = a[:, 2]
dy2 = b[:, 2]
int_a = intersectionFinder.findIntersection(x, y1, y2)
print(int_a)
c_int = int_a[0]
near_x = []
for ind,xval in enumerate(x):
    if xval > c_int[0]:
        near_x = [x[ind-1], x[ind]]
        near_y1 = [y1[ind-1], y1[ind]]
        near_y2 = [y2[ind-1], y2[ind]]
        near_del_1 = max([dy1[ind-1], dy1[ind]])
        near_del_2 = max([dy2[ind-1], dy2[ind]])
        break

if near_del_1 > near_del_2:
    slope = (near_y1[1] - near_y1[0])/(near_x[1] - near_x[0])
    delta_y = near_del_1
else:
    slope = (near_y2[1] - near_y2[0])/(near_x[1] - near_x[0])
    delta_y = near_del_2
delta_x = delta_y/slope

print('x ', c_int[0],delta_x, 'y ', c_int[1], delta_y)
