root_path = "/home/simon/exjobb/";
foutput_path = "/home/simon/exjobb/modular/foutput/";
scripts_path = "/home/simon/exjobb/scripts/";
pickles_path = "/home/simon/exjobb/modular/pickles/";
scripts_path = "~/exjobb/scripts/";
pickles_path = "~/exjobb/modular/pickles/";

def writeSelf(vals):
    with open("./settings.py","r") as fname:
        data = fname.readlines();
    data[0] = 'root_path = "'+vals[0]+'";\n';
    data[1] = 'foutput_path = "'+vals[1]+'";\n';
    data[2] = 'scripts_path = "'+vals[2]+'";\n';
    data[3] = 'pickles_path = "'+vals[3]+'";\n';
    with open("./settings.py","w") as fname:
        fname.writelines(data);

def set_values():
    root_path = input("path to exjobb dir");
    foutput_path = input("path to foutput");
    scripts_path = input("path to scripts");
    pickles_path = input("path to pickles");
    vals = [root_path,foutput_path,scripts_path,pickles_path];
    vals = [os.path.expanduser(x) for x in vals];
    writeSelf(vals);
if (__name__ == "__main__"):
    set_values()
