import numpy as np
import settings
from analysis import intersectionFinder

# import matplotlib.pyplot as plt
# import matplotlib.animation as animation


# format : L, L2, T, Bin_q, Rs_q, NL, NL2, dB, dR
#         0   1  2  3      4     5   6    7   8

# always returns only first intersection
def get_bin_rho_intersection(data_1, data_2):
    x = data_1[:, 2]
    y1_binder = data_1[:, 3]
    y2_binder = data_2[:, 3]
    y1_rho = data_1[:, 4]
    y2_rho = data_2[:, 4]
    bres = []
    rres = []
    intersection = intersectionFinder.findIntersection(x, y1_binder, y2_binder)

    if len(intersection) > 0:
        if len(intersection) > 1:
            print('more than 1 intersection binder')
            print(intersection)
        bres = intersection[0]
    else:
        bres = [np.nan, np.nan]
    rho_intersection = intersectionFinder.findIntersection(x, y1_rho, y2_rho)

    if len(rho_intersection) > 0:
        rres = rho_intersection[0]
        if len(intersection) > 1:
            print('more than 1 intersection rho')
            print(intersection)
    else:
        rres = [np.nan, np.nan]

    return [bres, rres]


def resale_quants(dat, omega):
    res = np.copy(dat)

    for i in range(dat.shape[0]):
        res[i, 3] = dat[i, 3] * np.float_power(dat[i, 0], omega)
        res[i, 4] = dat[i, 4] * np.float_power(dat[i, 0], omega)

    return res

def intersections_for_given_omega(data_size_1, data_size_2, omega):
    # format : L, L2, T, Bin_q, Rs_q, NL, NL2, dB, dR
    #         0   1  2  3      4     5   6    7   8
    size_1 = data_size_1[0, 0]
    size_2 = data_size_2[0, 0]


    scaled_data_1 = resale_quants(data_size_1, omega)
    scaled_data_2 = resale_quants(data_size_2, omega)
    intersections = get_bin_rho_intersection(scaled_data_1, scaled_data_2)
    return intersections
