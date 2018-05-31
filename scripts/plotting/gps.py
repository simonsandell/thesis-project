import os
import time
import subprocess
import sys
from tempfile import NamedTemporaryFile
import settings

def fileNotEmpty(fullpath):
    return (os.stat(fullpath).st_size != 0);
def initBat():
    t = NamedTemporaryFile("w",delete=False);
    t.write("#obligatory comment\n");
    return t;
def writeToBat(bfile,line):
    bfile.write(line + "\n");
def addFile(bfile,path,n):
    path = os.path.abspath(path);
    writeToBat(bfile,"READ BLOCK \"" + path + "\"");
    writeToBat(bfile,"BLOCK xydy \"1:2:3\"")
    writeToBat(bfile,"s" + str(n) + " line color " + str(1+(n%15)));
    writeToBat(bfile,"s" + str(n) + " symbol " + str(1+(n%11)));
    writeToBat(bfile,"s" + str(n) + " symbol size  0.5");
    writeToBat(bfile,"s" + str(n) + " legend \"" + os.path.basename(path) + "\"");
    writeToBat(bfile,"KILL BLOCK")

def graceDirPlot(directory,title, xaxis ,yaxis,xlog,ylog, doPrint,filefilter):
    nonEmpty = False;
    syscall = [];
    bfile = initBat();
    writeToBat(bfile,"XAXIS LABEL \"" + xaxis +"\"");
    writeToBat(bfile,"YAXIS LABEL \"" + yaxis +"\"");
    n = 0;
    for filename in sorted(os.listdir(directory)):
        if (filefilter in filename):
            if (os.stat(os.path.join(directory,filename)).st_size != 0):
                nonEmpty=True;
                if (doPrint):
                    if (".dat" in filename):
                        addFile(bfile,os.path.join(directory,filename),n)
                        n = n+1;
                else:
                    addFile(bfile,os.path.join(directory,filename),n);
                    n = n+1;
    if (nonEmpty):
        print(directory)
        if (xlog):
            writeToBat(bfile,"XAXES SCALE LOGARITHMIC");
            syscall.append( "-param");
            syscall.append(settings.scripts_path+"/plotting/logparams.par");
        if (ylog):
            writeToBat(bfile,"YAXES SCALE LOGARITHMIC");
        writeToBat(bfile,"LEGEND LENGTH 0");
        writeToBat(bfile,"AUTOSCALE");
        writeToBat(bfile,"AUTOTICKS");
        syscall.append("-batch");
        syscall.append(bfile.name);
        syscall.append("-nosafe");
        syscall.append("-noask");
        syscall.append("-free");
        if (doPrint):
            if (xlog or ylog):
                writeToBat(bfile,"LEGEND off");
            writeToBat(bfile,"PRINT TO \"" + title + ".eps\"");
            writeToBat(bfile,"HARDCOPY DEVICE \"EPS\"");
            writeToBat(bfile,"PAGE RESIZE 1920,1024");
            writeToBat(bfile,"DEVICE \"EPS\" FONT ANTIALIASING on");
            writeToBat(bfile,"PRINT");
            syscall = ["gracebat"] + syscall;
            bfile.flush();
            subprocess.call(syscall);
            del syscall[0];
        syscall = ["xmgrace"] + syscall;
        bfile.flush();
        subprocess.Popen(syscall);
        time.sleep(0.5);

def initAnim():
    subprocess.call(['rm','-r','/tmp/temppng'])
    subprocess.call(['mkdir','/tmp/temppng'])
def getOmega(filepath):
    f = open(filepath,"r");
    ln = f.read();
    ln = ln.rsplit(" ");
    return ln[-1].replace("\n","");
def setWorldView(bfile,model,quant):
    if (model == "Ising3D"):
        writeToBat(bfile,"WORLD XMIN 4.4850 ");
        writeToBat(bfile,"WORLD XMAX 4.515" );
        writeToBat(bfile,"WORLD YMIN -0.525" );
        writeToBat(bfile,"WORLD YMAX 1.15" );
    else:
        writeToBat(bfile,"WORLD XMIN 2.2015" );
        writeToBat(bfile,"WORLD XMAX 2.203" );
        if (quant == "RS"):
            writeToBat(bfile,"WORLD YMIN -0.5" );
            writeToBat(bfile,"WORLD YMAX 1.00" );
        else:
            writeToBat(bfile,"WORLD YMIN -0.5" );
            writeToBat(bfile,"WORLD YMAX 0.20" );


def graceAnimation(directory,aniname,xaxis,yaxis):
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
            bfile = initBat();
            n = 0;
            for f in sorted(os.listdir(os.path.join(directory,d))):
                fullpath = os.path.join(directory,d,f);
                if ( fileNotEmpty(fullpath)):
                    if (not hasOmega):
                        omega = getOmega(os.path.join(directory,d,f));
                    addFile(bfile,os.path.join(directory,d,f),n)
                    n = n+1;
            writeToBat(bfile,r'TITLE "\xw\0 = ' + str(omega)+ "\"");
            writeToBat(bfile,"XAXIS LABEL \"" + xaxis + "\"");
            writeToBat(bfile,"YAXIS LABEL \"" + yaxis + "\"");
            writeToBat(bfile,"AUTOSCALE ONREAD NONE");
            setWorldView(bfile,model,quant);
            writeToBat(bfile,"AUTOTICKS");
            writeToBat(bfile,"LEGEND ON ");
            writeToBat(bfile,"LEGEND LOCTYPE VIEW");
            writeToBat(bfile,"LEGEND 0.1,0.1");
            writeToBat(bfile,"PRINT TO \"/tmp/temppng/" + d + ".png\"");
            writeToBat(bfile,"HARDCOPY DEVICE \"PNG\"");
            writeToBat(bfile,"PAGE SIZE 1920,1024");
            writeToBat(bfile,"DEVICE \"PNG\" FONT ANTIALIASING on");
            writeToBat(bfile,"PRINT");
            subprocess.call(["gracebat","-batch",bfile.name,"-nosafe","-noask","-free"]);

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

#    writeToBat(bfile,"XAXIS LABEL \"" + xaxis + "\" ");
#    writeToBat(bfile,"YAXIS LABEL \"" + yaxis + "\" ");

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

