import os
root_path = "/home/simon/exjobb/";
foutput_path = "/home/simon/exjobb/modular/foutput/";
scripts_path = "/home/simon/exjobb/scripts/";
pickles_path = "/home/simon/exjobb/modular/pickles/";

def writeSelf(vals):
    with open("./settings.py","r") as fname:
        data = fname.readlines();
    data[1] = 'root_path = "'+vals[0]+'";\n';
    data[2] = 'foutput_path = "'+vals[1]+'";\n';
    data[3] = 'scripts_path = "'+vals[2]+'";\n';
    data[4] = 'pickles_path = "'+vals[3]+'";\n';
    with open("./settings.py","w") as fname:
        fname.writelines(data);

def set_values():
    r_path = input("path to exjobb dir");
    f_path = input("path to foutput");
    s_path = input("path to scripts");
    p_path = input("path to pickles");
    vals = [r_path,f_path,s_path,p_path];
    vals = [os.path.expanduser(x) for x in vals];
    writeSelf(vals);
if (__name__ == "__main__"):
    set_values()
