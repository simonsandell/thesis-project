import anaFuncs
fs= "{:30.30f}";

def stringBuilder(line):
    res = "";
    for word in line:
        res +=fs.format(word) +"    ";
    res += "\n";
    return res;



def writeDataTable(fName,model,array):
    openfile = open("./foutput/"+model+"/data_table_"+fName+"_.txt","w");
    openfile.write("# fName: " +fName +"\n");
    for ln in array:
        string = stringBuilder(ln);
        openfile.write(string);
    openfile.close();


def writeQuant(path,array,inds):
    [x,y,dy,n] = inds;
    of = open(path,"w");
    for i in range(array.shape[0]):
        line = [array[i,x],array[i,y],array[i,dy],array[i,n]];
        of.write(stringBuilder(line));

def writeVsT(fName,model,array):
    L = array[0,0];
    if (model == "3DXY"):
        idx = anaFuncs.get3DXYIndex();
        keys = ["b","rs","chi","dbdt","B","RS","CHI","C","DBDT","EN","MAG"];
        for key in keys:
            inds = [idx["T"],idx[key][0],idx[key][0] + idx["last"],idx["Nmcavg"]];
            dirname = idx[key][1];
            path = "./foutput/"+model+"/vsT/"+dirname+"/"+repr(L)+"_"+fName+"_"+key+".dat";
            writeQuant(path,array,inds);

def writeVsL(fName,model,array):
    T = array[0,1];
    if (model =="3DXY"):
        idx = anaFuncs.get3DXYIndex();
        keys = ["b","rs","chi","dbdt","B","RS","CHI","C","DBDT","EN","MAG"];
        for key in keys:
            inds = [idx["L"],idx[key][0],idx[key][0] + idx["last"],idx["Nmcavg"]];
            dirname = idx[key][1];
            path = "./foutput/"+model+"/vsL/"+dirname+"/"+repr(T)+"_"+fName+".dat";
            writeQuant(path,array,inds);
