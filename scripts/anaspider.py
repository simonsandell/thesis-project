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
doL = False;
doSC2 = False;
doSC3 = False;
doTeq = False;

doAna = True;
doPlot= False;
doPrint=False;

    



if (model == "3DXY"):
    xy3d.ana3DXY(fname,doTemp,doL,doSC2,doSC3,doTeq,doAna,doPlot,doPrint);
if (model == "Ising3D"):
    i3d.anaIsing3D(fname,doTemp,doL,doSC2,doSC3,doTeq,doAna,doPlot,doPrint);
    
