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
        print(string)
        openfile.write(string);
    openfile.close();



