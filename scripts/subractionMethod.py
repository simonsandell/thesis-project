import numpy as np
import settings
from plotting import fileWriter
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# load datatables, select temperature closest to T_L.
# for range of A, plot ln(quant - A) vs ln(L)
# determine A by slope, should be a constant function with slope equal to omega.

# put in new file?
# with the determined A, calculate omega directly as omega = -ln(y(2L)/y(L))/ln(2)


# for sequential L, calculate ln(y(2L)/y(L) = -omega*ln(2)

def func(x,a,b):
    return (a*np.e**(x*b));


def getTvalues(dt,T):
    Tv = np.unique(dt[:,1]);
    minDT = 10;
    closestT = 0;
    for t in Tv:
        if (abs(T-t) < minDT):
            minDT=abs(T-t);
            closestT = t;
    return dt[dt[:,1]==closestT];

savename = input("savename: ");
path  = settings.root_path+"modular/datatables/combined/";
# sorted by temp
datalist = [
        np.load(path +"datatable_4combined3DXY.npy"),
        np.load(path +"datatable_8combined3DXY.npy"),
        np.load(path +"datatable_16combined3DXY.npy"),
        np.load(path +"datatable_32combined3DXY.npy"),
        np.load(path +"datatable_64combined3DXY.npy"),
        np.load(path +"datatable_128combined3DXY.npy")];
T_L_B = 2.201909;
T_L_R = 2.2018832;
#take mean?
T_L = (T_L_B+T_L_R)/(2.0);

#
A_r_guess = 1.115775;
A_b_guess = 1.24805;
for i,dt in enumerate(datalist):
    datalist[i] = getTvalues(dt,T_L);

residualvsAb = [];
residualvsAr = [];
bin_vals =[];
rho_vals =[];
for factor in np.linspace(0.99,1.01,10):
    A_b = factor*A_b_guess;
    A_r = factor*A_r_guess;
    print(A_b)
    print(A_r)
    combined = np.empty((0,datalist[0].shape[1]));
    for dt in datalist:
        sub_dt = dt.copy();
        sub_dt[:,22] = sub_dt[:,22]-A_b; # B == 22
        sub_dt[:,26] = sub_dt[:,26]-A_r; # RS == 26
        combined = np.append(combined,sub_dt,axis=0);
    combined = combined[combined[:,0].argsort()];
    for i in range(combined.shape[0]):
        bin_vals.append([combined[i,0],combined[i,22],combined[i,22+30],A_b]);
        rho_vals.append([combined[i,0],combined[i,26],combined[i,26+30],A_r]);
    fileWriter.writeSubtractedQuants(savename+str(A_b),"bin",bin_vals);
    fileWriter.writeSubtractedQuants(savename+str(A_r),"rs",rho_vals);
    a,res,b,c,d = np.polyfit(np.log(combined[:,0]),np.log(-combined[:,22]),1,full=True);
    a,resr,b,c,d = np.polyfit(np.log(combined[:,0]),np.log(-combined[:,26]),1,full=True);

    cfb = curve_fit(func,combined[:,0],combined[:,22],full_output=1);
    cfr = curve_fit(func,combined[:,0],combined[:,26],full_output=1);
    print(cfb)

    residualvsAb.append([A_b,res]);
    residualvsAr.append([A_r,resr]);

    bin_vals[:] = [];
    rho_vals[:] = [];
fig = plt.figure()
axb = plt.subplot(211);
axr = plt.subplot(212);
resb = np.array(residualvsAb)
resr = np.array(residualvsAr)
print(resb)
print(resr)
axb.plot(resb[:,0],resb[:,1]);
axr.plot(resr[:,0],resr[:,1]);
plt.show();





