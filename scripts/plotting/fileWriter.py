import anaFuncs
import settings

fs = "{:30.30f}"
s = "/"
u = "_"


def stringBuilder(line):
    res = ""
    for word in line:
        res += fs.format(word) + "    "
    res += "\n"
    res = res.replace("inf", "0.0")
    res = res.replace("nan", "0.0")
    return res


def writeDataTable(fName, array):
    openfile = open(
        settings.foutput_path + settings.model + "/datatable_" + fName + "_.txt", "w"
    )
    openfile.write("# fName: " + fName + "\n")
    for ln in array:
        string = stringBuilder(ln)
        openfile.write(string)
    openfile.close()


def writeQuantClean(path, array, inds):
    [x, y, dy, n] = inds
    of = open(path, "w")
    for i in range(array.shape[0]):
        line = [array[i, x], array[i, y], array[i, dy], array[i, n]]
        if (not ("inf" in line)) and (not ("nan" in line)):
            of.write(stringBuilder(line))


def writeQuant(path, array, inds):
    [x, y, dy, n] = inds
    of = open(path, "w")
    for i in range(array.shape[0]):
        line = [array[i, x], array[i, y], array[i, dy], array[i, n]]
        of.write(stringBuilder(line))


def writeQuantNoDY(path, array, inds):
    [x, y] = inds
    of = open(path, "w")
    for i in range(array.shape[0]):
        line = [array[i, x], array[i, y], 0.0]
        of.write(stringBuilder(line))


def writeVsT(savename, array):
    L = array[0, 0]
    if settings.model == "3DXY":
        idx = anaFuncs.get3DXYIndex()
        keys = ["b", "rs", "chi", "dbdt", "B", "RS", "CHI", "C", "DBDT", "EN", "MAG"]
        for key in keys:
            inds = [idx["T"], idx[key][0], idx[key][0] + idx["last"], idx["Nmcavg"]]
            dirname = idx[key][1]
            path = (
                settings.foutput_path
                + settings.model
                + "/vsT/"
                + dirname
                + "/"
                + savename
                + u
                + key
                + ".dat"
            )
            writeQuant(path, array, inds)


def writeVsL(savename, array):
    if settings.model == "3DXY":
        idx = anaFuncs.get3DXYIndex()
        keys = ["b", "rs", "chi", "dbdt", "B", "RS", "CHI", "C", "DBDT", "EN", "MAG"]
        array[:, idx["EN"][0]] = -array[:, idx["EN"][0]]
        for key in keys:
            inds = [idx["L"], idx[key][0], idx[key][0] + idx["last"], idx["Nmcavg"]]
            dirname = idx[key][1]
            path = (
                settings.foutput_path
                + settings.model
                + "/vsL/"
                + dirname
                + "/"
                + savename
                + u
                + key
                + ".dat"
            )

            writeQuant(path, array, inds)


def writeOmegaVsClose(savename, dirname, data):
    of = open(
        settings.foutput_path
        + settings.model
        + s
        + "vsO/"
        + dirname
        + s
        + savename
        + ".dat",
        "w",
    )
    for line in data:
        of.write(stringBuilder(line))


# produce [T, omegabin, omegarho, L1,L2,L3,N1,N2,N3,domegabin,domegarho,]
def writeThreeLMethod(savename, result):
    if settings.model == "3DXY":
        binof = open(
            settings.foutput_path
            + settings.model
            + s
            + "threeL/bin/"
            + savename
            + ".dat",
            "w",
        )
        rhoof = open(
            settings.foutput_path
            + settings.model
            + s
            + "threeL/rs/"
            + savename
            + ".dat",
            "w",
        )
        for ln in result:
            bln = [ln[0], ln[1], ln[9], *ln[3:9]]
            rln = [ln[0], ln[2], ln[10], *ln[3:9]]
            fbl = stringBuilder(bln)
            frl = stringBuilder(rln)
            if not "nan" in fbl:
                binof.write(fbl)
            if not "nan" in frl:
                rhoof.write(frl)


def writeQuantInt(savename, data):
    if settings.model == "3DXY":
        if "bin" in savename:
            of = open(
                settings.foutput_path
                + settings.model
                + "/intersections/bin/"
                + savename
                + ".dat",
                "w",
            )
        if "rho" in savename:
            of = open(
                settings.foutput_path
                + settings.model
                + "/intersections/rs/"
                + savename
                + ".dat",
                "w",
            )
        for ln in data:
            of.write(stringBuilder(ln))


def writeSubtractedQuants(savename, dirname, data):
    of = open(
        settings.foutput_path
        + settings.model
        + "/subtraction/"
        + dirname
        + "/"
        + savename
        + ".dat",
        "w",
    )
    for ln in data:
        of.write(stringBuilder(ln))
