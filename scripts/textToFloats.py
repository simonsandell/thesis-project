
# N_vals = 22 for 3DXY, 19 for Ising3D
def loadData(path,N_vals):
    data = [];
    datafile = open(path,"r");
    i = 0;
    for ln in datafile:
        i = i+1;
        if not (('#' in ln) or ('WORLD' in ln) or ('SEED' in ln) or ('aprun' in ln)):
            strlist = ln.rsplit(" ");
            strlist = [x for x in strlist if not (x== "\n")];
            try:
                fllist = [float(x) for x in strlist];
                if (len(fllist) != N_vals):
                    print(path)
                    print(len(strlist));
                    print('bad line at row ' + str(1 + i));
                else:
                    data.append(fllist);
            except:
                print(path);
                print('bad line at row ' + str(1 + i));
    return data;
