import os
root_path = "/home/simon/exjobb/";
foutput_path = "/home/simon/exjobb/modular/foutput/";
scripts_path = "/home/simon/exjobb/scripts/";
pickles_path = "/home/simon/exjobb/modular/pickles/";
model = "3DXY";

def writeSelf(vals):
    with open("./settings.py","r") as fname:
        data = fname.readlines();
    data[1] = 'root_path = "'+vals[0]+'";\n';
    data[2] = 'foutput_path = "'+vals[1]+'";\n';
    data[3] = 'scripts_path = "'+vals[2]+'";\n';
    data[4] = 'pickles_path = "'+vals[3]+'";\n';
    data[5] = 'model = "'+vals[4]+'";\n';
    with open("./settings.py","w") as fname:
        fname.writelines(data);

def set_values():
    r_path = input("path to root: ");
    f_path = input("relpath to foutput: ");
    s_path = input("relpath to scripts: ");
    p_path = input("relpath to pickles: ");
    model = input("model: ");
    vals = [r_path,r_path+f_path,r_path+s_path,r_path+p_path,model];
    vals = [os.path.expanduser(x) for x in vals];
    writeSelf(vals);
if (__name__ == "__main__"):
    set_values()
