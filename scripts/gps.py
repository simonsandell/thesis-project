import os
import time
import subprocess
import sys
def fileNotEmpty(fullpath):
    return (os.stat(fullpath).st_size != 0);
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
    initBat();
    writeToBat("XAXIS LABEL \"" + xaxis +"\"");
    writeToBat("YAXIS LABEL \"" + yaxis +"\"");
    n = 0;
    for filename in sorted(os.listdir(directory)):
        print(filename)
        if (os.stat(os.path.join(directory,filename)).st_size != 0):
            if (doPrint):
                if (".dat" in filename):
                    addFile(os.path.join(directory,filename),n)
                    n = n+1;
            else:
                addFile(os.path.join(directory,filename),n);
                n = n+1;
    if (logPlot):
        writeToBat("XAXES SCALE LOGARITHMIC");
        writeToBat("YAXES SCALE LOGARITHMIC");
    writeToBat("LEGEND LENGTH 0");
    writeToBat("AUTOSCALE");
    writeToBat("AUTOTICKS");
    if (doPrint):
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

def initAnim():
    subprocess.call(['rm','-r','/tmp/temppng'])
    subprocess.call(['mkdir','/tmp/temppng'])
def getOmega(filepath):
    f = open(filepath,"r");
    ln = f.read();
    ln = ln.rsplit(" ");
    return ln[-1].replace("\n","");
def setWorldView(model,quant):
    if (model == "Ising3D"):
        writeToBat("WORLD XMIN 4.4850 ");
        writeToBat("WORLD XMAX 4.515" );
        writeToBat("WORLD YMIN -0.525" );
        writeToBat("WORLD YMAX 1.15" );
    else:
        writeToBat("WORLD XMIN 2.2015" );
        writeToBat("WORLD XMAX 2.203" );
        if (quant == "RS"):
            writeToBat("WORLD YMIN -0.5" );
            writeToBat("WORLD YMAX 1.00" );
        else:
            writeToBat("WORLD YMIN -0.5" );
            writeToBat("WORLD YMAX 0.20" );


def graceAnimation(directory,aniname,xaxis,yaxis):
    print(directory)
    if ("3DXY" in directory):
        model = "3DXY";
        if ("RS" in directory):
            quant = "RS";
        else:
            quant = "B";
    else:
        quant = "B";
        model = "Ising3D";
    initAnim();
    hasOmega = False;
    omega = 0;
    for subdirs, dirs, files in os.walk(directory):
        for d in sorted(dirs): 
            initBat();
            n = 0;
            for f in sorted(os.listdir(os.path.join(directory,d))):
                fullpath = os.path.join(directory,d,f);
                if ( fileNotEmpty(fullpath)):
                    if (not hasOmega):
                        omega = getOmega(os.path.join(directory,d,f));
                    addFile(os.path.join(directory,d,f),n)
                    n = n+1;
            writeToBat(r'TITLE "\xw\0 = ' + str(omega)+ "\"");
            writeToBat("XAXIS LABEL \"" + xaxis + "\"");
            writeToBat("YAXIS LABEL \"" + yaxis + "\"");
            writeToBat("AUTOSCALE ONREAD NONE");
            setWorldView(model,quant);
            writeToBat("AUTOTICKS");
            writeToBat("LEGEND ON ");
            writeToBat("LEGEND LOCTYPE VIEW");
            writeToBat("LEGEND 0.1,0.1");
            writeToBat("PRINT TO \"/tmp/temppng/" + d + ".png\"");
            writeToBat("HARDCOPY DEVICE \"PNG\"");
            writeToBat("PAGE SIZE 1920,1024");
            writeToBat("DEVICE \"PNG\" FONT ANTIALIASING on");
            writeToBat("PRINT");
            subprocess.call(["gracebat","-batch","/tmp/setup.batch","-nosafe","-noask","-free"]);

    subprocess.call(['convert -delay 100 /tmp/temppng/*.png gif:./foutput/animations/'+aniname+'.gif'],shell=True);
    subprocess.Popen(['eog','./foutput/animations/'+aniname+'.gif']);





#!/bin/bash
#filedir=$1
#outputfile="./foutput/animations/$2.gif"
#pngdir=./tempdir
#mkdir $pngdir 
#for subdir in $filedir/*/; do
#	string="-legend load";
#	omega=""
#	for file in $subdir*.dat; do
#		if [ -z "$omega" ]; then
#	      		omega=$(head -n 1 $file | awk -F' ' '{ print $4 }' )
#		fi
#		string="$string -settype xydy $file"
#	done
#	rm ../scripts/setup.batch
#	echo "XAXIS LABEL \"Temperature\" " > ../scripts/setup.batch
#	echo "YAXIS LABEL \"L\S\xw\0\N\c7\C[2L\c7\C\xr\0\ss\N(2L) - \L\c7\C\xr\0\ss\N(L)]\" " >> ../scripts/setup.batch
#	echo "YAXIS TICK MAJOR 0.05 " >> ../scripts/setup.batch
#	echo "YAXIS TICK MINOR 0.025 " >> ../scripts/setup.batch
#	echo "TITLE \"\xw = $omega\" " >> ../scripts/setup.batch
#	echo "AUTOSCALE ONREAD NONE" >> ../scripts/setup.batch
#	echo "WORLD XMIN 4.4850 " >> ../scripts/setup.batch #read these from file?
#	echo "WORLD XMAX 4.515" >> ../scripts/setup.batch
#	echo "WORLD YMIN -0.525" >> ../scripts/setup.batch
#	echo "WORLD YMAX 1.15" >> ../scripts/setup.batch
#	echo "LEGEND ON " >> ../scripts/setup.batch
#	echo "LEGEND LOCTYPE WORLD" >> ../scripts/setup.batch
#	echo "LEGEND 4.485, 1.14 " >> ../scripts/setup.batch
#	gracebat -batch ../scripts/setup.batch $string  -nosafe -printfile $pngdir/$(basename $subdir).png -hdevice PNG -hardcopy  
#done
#convert -delay 50 $pngdir/*.png $outputfile
#eog $outputfile &
#rm -r $pngdir

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

