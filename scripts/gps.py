import os
import time
import subprocess
import sys
def initBat():
    subprocess.call(["rm","-f","/tmp/setup.batch"]);
    bf = open("/tmp/setup.batch","a")
    bf.write("#obligatory comment\n");
def writeToBat(line):
    bfile = open("/tmp/setup.batch","a");
    bfile.write(line + "\n");
def addFile(path,n):
    path = os.path.abspath(path);
    writeToBat("READ BLOCK \"" + path + "\"");
    writeToBat("BLOCK xydy \"1:2:3\"")
    writeToBat("s" + str(n) + " line color " + str(1+(n%15)));
    writeToBat("s" + str(n) + " symbol " + str(1+(n%11)));
    writeToBat("s" + str(n) + " symbol size  0.5");
    writeToBat("s" + str(n) + " legend \"" + os.path.basename(path) + "\"");
    writeToBat("KILL BLOCK")

def graceDirPlot(directory,title, xaxis ,yaxis,logPlot, doPrint):
    graceExe = "xmgrace"
    initBat();
    writeToBat("XAXIS LABEL \"" + xaxis +"\"");
    writeToBat("YAXIS LABEL \"" + yaxis +"\"");
    n = 0;
    for filename in os.listdir(directory):
        print(os.path.join(directory,filename))
        if (os.stat(os.path.join(directory,filename)).st_size != 0):
            print(os.stat(os.path.join(directory,filename)).st_size)
            addFile(os.path.join(directory,filename),n)
            n = n+1;
    if (logPlot):
        writeToBat("XAXES SCALE LOGARITHMIC");
        writeToBat("YAXES SCALE LOGARITHMIC");
    writeToBat("LEGEND LENGTH 0");
    writeToBat("AUTOSCALE");
    writeToBat("AUTOTICKS");
    if (doPrint):
        graceExe = "gracebat"
        if (logPlot):
            writeToBat("LEGEND off");
        writeToBat("PRINT TO \"" + title + ".eps\"");
        writeToBat("HARDCOPY DEVICE \"EPS\"");
        writeToBat("PAGE RESIZE 1920,1024");
        writeToBat("DEVICE \"EPS\" FONT ANTIALIASING on");
        writeToBat("PRINT");
        subprocess.call(["gracebat","-batch","/tmp/setup.batch","-nosafe","-noask","-free"]);
    else:
        subprocess.Popen(["xmgrace","-batch","/tmp/setup.batch","-nosafe","-noask","-free"]);
        time.sleep(0.5);





#    writeToBat("XAXIS LABEL \"" + xaxis + "\" ");
#    writeToBat("YAXIS LABEL \"" + yaxis + "\" ");

#    AUTOSCALE
#    PRINT TO "histogram.png"
#    HARDCOPY DEVICE "PNG"
#    PAGE SIZE 2560, 2048
#    DEVICE "PNG" FONT ANTIALIASING on
#    DEVICE "PNG" OP "transparent:on"
#    DEVICE "PNG" OP "compression:9"
#    PRINT

#   READ NXY "5M030.rmsd1.txt"
#   READ NXY "5M030.rmsd2.txt"
#   s0 line color 1
#   s1 line color 2
#   s0 legend "pose1 rmsd"
#   s1 legend "pose2 rmsd"
#   title "RMSD"
#   xaxis label "time (ps)"
#   yaxis label "RMSD (angstroms)"
#   PRINT TO "${system}.eps"
#   DEVICE "EPS" OP "level2"
#   PRINT TO "histogram.png"
#   HARDCOPY DEVICE "PNG"
#   PAGE SIZE 2560, 2048
#   DEVICE "PNG" FONT ANTIALIASING on
#   DEVICE "PNG" OP "transparent:on"
#   DEVICE "PNG" OP "compression:9"
#   PRINT   PRINT

