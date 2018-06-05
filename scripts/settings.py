import os
root_path = "/home/simon/exjobb/";
foutput_path = "/home/simon/exjobb/modular/foutput/";
scripts_path = "/home/simon/exjobb/scripts/";
pickles_path = "/home/simon/exjobb/modular/pickles/";
datatables_path = "/home/simon/exjobb/modular/datatables/";
model = "3DXY";
nprocs = 2;

def writeSelf(vals):
    with open("./settings.py","r") as fname:
        data = fname.readlines();
    data[1] = 'root_path = "'+vals[0]+'";\n';
    data[2] = 'foutput_path = "'+vals[1]+'";\n';
    data[3] = 'scripts_path = "'+vals[2]+'";\n';
    data[4] = 'pickles_path = "'+vals[3]+'";\n';
    data[5] = 'datatables_path = "'+vals[4]+'";\n';
    data[6] = 'model = "'+vals[5]+'";\n';
    data[7] = 'nprocs = '+vals[6]+';\n';
    with open("./settings.py","w") as fname:
        fname.writelines(data);

def set_values():
    r_path = input("path to root: ");
    f_path = input("relpath to foutput: ");
    s_path = input("relpath to scripts: ");
    p_path = input("relpath to pickles: ");
    d_path = input("relpath to datatables: ");
    model = input("model: ");
    nproc = input("nprocs: ");
    vals = [r_path,r_path+f_path,r_path+s_path,r_path+p_path,r_path+d_path,model,nproc];
    vals = [os.path.expanduser(x) for x in vals];
    writeSelf(vals);
if (__name__ == "__main__"):
    set_values()
