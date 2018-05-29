import numpy as np
import matplotlib.pyplot as plt

def calcIntersection(y11,y12,y21,y22,dT):
    return dT*(y21 - y11)/(y12 + y21 - y11 - y22);

def intersects(mat,i,j,n):
    ydiff_1 = mat[i,3]  - mat[j,3];
    ydiff_2 = mat[i,3]  - mat[j,3];

def testIntersection(mat,midind,Tc):
    dT = mat[midind,2] - mat[0,2];
    for i in range(N_temps -1):
        for j in range(N_temps -1 -i):
            ydiff_1  = mat[i,3] - mat[i+j,3];
            ydiff_2 = mat[i+N_temps] - mat[i+j+N_temps,3];
            if (ydiff_1*ydiff_2 >0):
                return -1;
            else:
                x = calcIntersection(mat[i,3],mat[i+N_temps,3],mat[i+j,3],mat[i+j+N_temps,3],dT);
                if ((abs(x -Tc)/(Tc)) < 0.1)):
                    return x;
                else:
                    print("intersection far away from guess: "+ str(x));
                    return x;

def findIntersections(mat,Tc):
    ret = [];
    tval,tind = np.unique(mat[:,2],return_index=True);
    tind = np.append(tind,mat.shape[0]);
    for i in range(len(tval) -1):
        N_temps = tind[i+1] - tind[i] +1;
        N_temps2 = tind[i+2] - tind[i+1] +1;
        if (N_temps != N_temps2):
            print("findBestIntersection: not consistent temperatures");
        testInt = testIntersection(mat[tind[i]:tind[i+2],:],N_temps,Tc);
        if (testInt != -1):
            ret.append(testInt);
    if (len(ret) >0):
        return ret;
    else:
        return -1;
        

    



def analyze(mat,fName,dirname,Tcguess):
    mat = np.array(mat);
    ind = np.lexsort((mat[:,0],mat[:,2],mat[:,5]));
    # mat contains [Ls[0],Ls[1],T,quant,delta,omega];
    # small L, big L, Temp, scalingquant, delta, omega.
    #       0      1     2             3      4      5
    mat = mat[ind];

    doPlot = input("findIntersection: Plot?");
    if ( doPlot == "y" or doPlot == "Y"):
        doPlot = True;
    else:
        doPlot = False;
    oval,oind = np.unique(mat[:,5],return_index=True); 
    oind = np.append(oind,mat.shape[0]);

    intersections =[];
    for i in range(len(oval)):
        tryfind = findIntersections(mat[oind[i]:oind[i+1],:],Tc);
        if (tryfind != -1):
            intersections.append(tryfind);
        if (doPlot):
            plt.cla()
            plt.gca().set_title("w = " + str(omega));
            for i in range(len(linds)-1):
                plt.plot(mat[linds[i]:linds[i+1],2],mat[linds[i]:linds[i+1],3]);
            x=[];
            y=[];
            #xmn = 10;
            #xmx = 0;
            #ymn = 10;
            #ymx = 0;
    
            for i in range(len(ints)):
                x.append(ints[i][0]);
                y.append(ints[i][1]);
            #    if (x[i] > xmx):
            #        xmx = x[i];
            #    if (x[i] < xmn):
            #        xmn = x[i];
            #    if (y[i] > ymx):
            #        ymx = y[i];
            #    if (y[i] < ymn):
            #        ymn = y[i];
            #xmx += 0.1*(xmx-xmn);
            #ymx += 0.1*(ymx-ymn);
            #xmn -= 0.1*(xmx-xmn);
            #ymn -= 0.1*(ymx-ymn);
            #plt.gca().set_xlim(left=xmn,right=xmx);
            #plt.gca().set_ylim(top=ymn,bottom=ymx);
            
            plt.scatter(x,y);
            plt.gca().set_xlim(left=2.20185,right=2.20205);
            plt.gca().set_ylim(top=1,bottom=0);
            plt.show(block=False);
            plt.pause(0.2);
    
    
    
    
    
        
    
