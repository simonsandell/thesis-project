import ana3DXY as xy3d
import anaIsing3D as i3d
import sys
import plotter

ans = [];
model = [];
if (len(sys.argv) < 3):
    default = input("default?");
    if (default == "Y" or default == "y"):
        plotter.plot3DXY();

    else:

        fName = input("filename? ");
        inputs = ["model  ? ","doTemp ? ", "doL    ? ","doSC2  ? ","doSC3  ? ","doTeq  ? ","doAna  ? ","doPlot ? ","doPrint? "]
        for ln in inputs:
            a = input(ln);
            if (a == "3DXY"):
                model = xy3d;
            elif (a == "Ising3D"):
                model = i3d;
            elif (a =="y" or a == "Y"):
                ans.append(True);
            else:
                ans.append(False);
else    :
        print(sys.argv)
        fName = sys.argv[1];
        if (sys.argv[2] == "3DXY"):
            model = xy3d;
        elif(sys.argv[2] == "Ising3D"):
            model = i3d;
        ans = [fName,True,True,True,True,False,True,False,False];
        model.ana(*ans);
