import plot_dicts
class plot_params:
    xlabel,ylabel,title = "", "", ""
    xlog, ylog = False, False

    def __init__(self, path):
        self.xlabel = plot_dicts.dict_xaxis[path]
        self.ylabel = plot_dicts.dict_yaxis[path]
        self.title = plot_dicts.dict_title[path]

        for k in plot_dicts.dict_log:
            if path in plot_dicts.dict_log[k]:
                self.xlog,self.ylog = k

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
