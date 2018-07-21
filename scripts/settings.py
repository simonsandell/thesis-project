import os
root_path = "/home/simon/exjobb/"
foutput_path = "/home/simon/exjobb/modular/foutput/"
scripts_path = "/home/simon/exjobb/scripts/"
pickles_path = "/home/simon/exjobb/modular/pickles/"
datatables_path = "/home/simon/exjobb/modular/datatables/"
model = "3DXY"
nprocs = 2


#######
## Current datatables
#######
TAG = "jul_20"

DATATABLES = [
    datatables_path + "July_20_2018/datatable_4.0jul53DXY.npy",
    datatables_path + "July_20_2018/datatable_8.0jul53DXY.npy",
    datatables_path + "July_20_2018/datatable_16.0jul53DXY.npy",
    datatables_path + "July_20_2018/datatable_32.0jul_203DXY.npy",
    datatables_path + "July_20_2018/datatable_64.0jul_203DXY.npy",
    datatables_path + "July_20_2018/datatable_128.0jul_203DXY.npy",
]

JACKTABLES = [
    datatables_path + "July_20_2018/jackknife/4combined_nf.npy",
    datatables_path + "July_20_2018/jackknife/8combined_nf.npy",
    datatables_path + "July_20_2018/jackknife/16combined_nf.npy",
    datatables_path + "July_20_2018/jackknife/32combined_nf.npy",
    datatables_path + "July_20_2018/jackknife/64combined_nf.npy",
    datatables_path + "July_20_2018/jackknife/128combined_nf.npy",
]

def write_self(vals):
    with open("./settings.py", "r") as fname:
        data = fname.readlines()
    data[1] = 'root_path = "' + vals[0] + '"\n'
    data[2] = 'foutput_path = "' + vals[1] + '"\n'
    data[3] = 'scripts_path = "' + vals[2] + '"\n'
    data[4] = 'pickles_path = "' + vals[3] + '"\n'
    data[5] = 'datatables_path = "' + vals[4] + '"\n'
    data[6] = 'model = "' + vals[5] + '"\n'
    data[7] = "nprocs = " + vals[6] + "\n"
    with open("./settings.py", "w") as fname:
        fname.writelines(data)


def set_values():
    r_path = input("path to root: ")
    f_path = input("relpath to foutput: ")
    s_path = input("relpath to scripts: ")
    p_path = input("relpath to pickles: ")
    d_path = input("relpath to datatables: ")
    mod = input("model: ")
    nproc = input("nprocs: ")
    vals = [
        r_path,
        r_path + f_path,
        r_path + s_path,
        r_path + p_path,
        r_path + d_path,
        mod,
        nproc,
    ]
    vals = [os.path.expanduser(x) for x in vals]
    write_self(vals)


if __name__ == "__main__":
    set_values()
