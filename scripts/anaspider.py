import ana3DXY as xy3d
import anaIsing3D as i3d
import sys


model =sys.argv[1];
fname = sys.argv[2];
if (len(sys.argv)> 3):
    preset = sys.argv[3];
else: 
    preset = "defualt";


doTemp = True;
doL = True;
doSC2 = False;
doSC3 = True;
doTeq = False;

doAna = False;
doPlot= True;
doPrint=True;

if (preset ==  "plot"):
    doAna=False;
    doPrint=False;
if (preset ==  "all"):
    doSC2 = True;
    doAna =True;
if (preset == "teq"):
    doTemp = False;
    doL = False;
    doSC3 = False;

    doAna = True;
    doTeq = True;
    



if (model == "3DXY"):
    xy3d.ana3DXY(fname,doTemp,doL,doSC2,doSC3,doTeq,doAna,doPlot,doPrint);
if (model == "Ising3D"):
    i3d.anaIsing3D(fname,doTemp,doL,doSC2,doSC3,doTeq,doAna,doPlot,doPrint);
    
