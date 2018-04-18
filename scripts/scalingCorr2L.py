import os
import math
import subprocess
import numpy as np
import jackknife

def openFiles(dirname,omega):
    ofile = open(dirname+"/omega_"+str(omega)+"_.dat","w");
    return ofile;

    
def calculate(mat,omega,istart,iend,ofile,function):
    quant = function(mat[istart:iend,:],omega);
    #delta = jackknife.getJackDelta(mat[istart:iend,:],lambda x: function(x,omega),100)[0];
    delta = 0.00;
        
    fstr= "{:30.30f}";
    ostr = "{:.5f}";
    Ls = np.unique(mat[istart:iend,0]);
    T = mat[istart,1];
    ofile.write(fstr.format(Ls[0]) + "    " + 
                fstr.format(Ls[1])+  "    " + 
                fstr.format(T)+      "    " +
                fstr.format(quant)+  "    " +
                fstr.format(delta)+  "    " +
                ostr.format(omega)+  "\n");



    
def analyze(mat,dirname,function,orange):
    #sort indata by T first , then L.
    ind = np.lexsort((mat[:,0],mat[:,1]));
    smat = mat[ind];
    
    #define range of omegas

    T_vals,T_inds = np.unique(smat[:,1],return_index=True);
    T_inds = np.append(T_inds,smat.shape[0]);
    print("Number of temps in sc2 " + str(len(T_vals)));
    
    for n in range(len(orange)):
        omega = orange[n];
        ofile= openFiles(dirname,omega);
        print(omega);
        for i in range(len(T_vals)): 
            L_vals,L_inds = np.unique(smat[T_inds[i]:T_inds[i+1],0],return_index=True);
            L_inds = np.append(L_inds,T_inds[i+1]-T_inds[i]);
            N_L = len(L_vals);
            N_lines = N_L -1;
            if (N_lines > 0):
                for j in range(N_lines):
                   calculate(smat,omega,T_inds[i]+L_inds[j],T_inds[i]+L_inds[j+2],ofile,function);



