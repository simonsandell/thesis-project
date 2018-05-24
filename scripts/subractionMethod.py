import numpy as np
import settings
# load datatables, select temperature closest to T_L.
# for range of A, plot ln(quant - A) vs ln(L)
# determine A by slope, should be a constant function with slope equal to omega.

# put in new file?
# with the determined A, calculate omega directly as omega = -ln(y(2L)/y(L))/ln(2)


# for sequential L, calculate ln(y(2L)/y(L) = -omega*ln(2)

path  = settings.root_path+"modular/datatables/combined/";
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

for factor in np.arange(0.9,1.1,30):
    A_b = factor*A_b_guess;
    A_r = factor*A_r_guess;
    for dt1,dt2 in zip(datalist[:-1],datalist[1:]):
        sub_dt1 = dt1.copy();
        sub_dt2 = dt2.copy();
        sub_dt1[:,binder] = sub_dt1[:,binder] - A_b;
        sub_dt2[:,binder] = sub_dt2[:,binder] - A_b;
        sub_dt1[:,rho] = sub_dt1[:,rho] - A_r;
        sub_dt2[:,rho] = sub_dt2[:,rho] - A_r;


#Then, compare closeness of intersection points vs A in a plot.
