import ana3DXY as xy3d
import anaIsing3D as i3d
import sys

fName = input("filename? ");
inputs = ["model  ? ","doTemp ? ", "doL    ? ","doSC2  ? ","doSC3  ? ","doTeq  ? ","doAna  ? ","doPlot ? ","doPrint? "]
ans = [];
model = [];
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
model.ana(fName,ans[0],ans[1],ans[2],ans[3],ans[4],ans[5],ans[6],ans[7]);
