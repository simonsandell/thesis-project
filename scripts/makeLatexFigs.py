import os

def initFile():
    f = open("figures.tex","w");
    return f;

def writeFig(filepath,cap,f):
    f.write(r'\begin{figure}[!htpb]' + "\n")
    f.write(r'  \centering' + "\n")
    f.write(r'  \includegraphics[width=15cm]{' + filepath + r'}' + "\n")
    f.write(r'  \caption{' + cap + r'}' + "\n")
    f.write(r'\end{figure}' + "\n")
    f.write("\n");



directory = "."
writefile = initFile();
for subdirs,dirs, files in os.walk(directory):
    for f in files:
        if (".eps" in f):
            if ("3DXY" in subdirs):
                cap = "3DXY";
                writeFig(os.path.join(subdirs,f),cap,writefile)
            if ("Ising3D" in subdirs):
                cap = "Ising3D";
                writeFig(os.path.join(subdirs,f),cap,writefile)

    
