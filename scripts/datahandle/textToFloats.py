# n_vals = 22 for 3DXY, 19 for Ising3D
def loadData(path, n_vals, enf_enc = False):
    data = []
    if enf_enc:
        datafile = open(path, "r", encoding='utf-8')
    else:
        datafile = open(path, "r")

    i = 0
    for line in datafile:
        i = i + 1
        if not (("#" in line) or ("WORLD" in line) or ("SEED" in line) or ("aprun" in line)):
            strlist = line.rsplit(" ")
            strlist = [x for x in strlist if not x == "\n"]
            try:
                fllist = [float(x) for x in strlist]
                if len(fllist) != n_vals:
                    print(path)
                    print(len(strlist))
                    print("bad line at row " + str(1 + i))
                else:
                    data.append(fllist)
            except:
                print(path)
                print("bad line at row " + str(1 + i))
    return data
