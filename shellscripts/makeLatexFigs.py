import os

def initFile():
    f = open("figures.tex","w");
    return f;

def writeFig(filepath,cap,f,filename):
    f.write(r'\begin{figure}[!htpb]' + "\n")
    f.write(r'  \centering' + "\n")
    f.write(r'  \includegraphics[width=\textwidth]{' + filepath + r'}' + "\n")
    f.write(r'  \caption{' + cap + " " +filename.replace("_"," ").replace(".eps","") +  r'}' + "\n")
    f.write(r'\end{figure}' + "\n")
    f.write("\n");



directory = "."
writefile = initFile();
for files in os.listdir(directory):
    if (".eps" in files):
        cap = "autogen";
        writeFig("./plots/" + files, cap, writefile, files)

    
