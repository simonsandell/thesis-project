import anaFuncs
import settings
fs= "{:30.30f}";

def stringBuilder(line):
    res = "";
    for word in line:
        res +=fs.format(word) +"    ";
    res += "\n";
    return res;

def writeDataTable(fName,model,array):
    openfile = open(settings.foutput_path+model+"/datatable_"+fName+"_.txt","w");
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
            path = settings.foutput_path+model+"/vsT/"+dirname+"/"+repr(L)+"_"+fName+"_"+key+".dat";
            writeQuant(path,array,inds);

def writeVsL(fName,model,array):
    T = array[0,1];
    if (model =="3DXY"):
        idx = anaFuncs.get3DXYIndex();
        keys = ["b","rs","chi","dbdt","B","RS","CHI","C","DBDT","EN","MAG"];
        for key in keys:
            inds = [idx["L"],idx[key][0],idx[key][0] + idx["last"],idx["Nmcavg"]];
            dirname = idx[key][1];
            path = settings.foutput_path+model+"/vsL/"+dirname+"/"+repr(T)+"_"+fName+".dat";
            writeQuant(path,array,inds);

def write2LData(f1,f2,model,data):
    if (model == "3DXY"):
        u = "_";
        of = open(settings.foutput_path+"3DXY/2LDT"+u+model+u+f1+u+f2+".txt","w");
        of.write("# L L2 T Bin Rs NL NL2 dBin dRs \n");
        for ln in data:
            of.write(stringBuilder(ln));


