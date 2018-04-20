
def getOmegaRange(ostart,oend,step):
    omegarange = [];
    omega = ostart;
    omegarange.append(ostart);
    while (omega < oend):
        omega = omega + step;
        omegarange.append(omega);
    return omegarange;

def dirToYaxis(dirname):
    dirLex = { 'en':r'e Energy per spin',
            'mag':r'm Magnetization per spin',
            'bin':r'B = M\S4\N/M\S2\N',
            'dbdt':r'dB/dT',
            'xi':r'\xc\0 Susceptibility',
            'rs':r'L\xr\0\ss\N Superfluid density',
            'm2':r'm\S2\N',
            'm4':r'm\S4\N',
            'c':'C - Heat Capacity',
            'omegaBin3L':r'\xw\0 = -ln(B(4L) - B(2L)/B(2L) - B(L))/ln(2)',
            'omegaRS3L':r'\xw\0 = -ln(\xr\0\ss\N(4L) - \xr\0\ss\N(2L)/\xr\0\ss\N(2L) - \xr\0\ss\N(L))/ln(2)',
            'omegaBin2L':r'L\S\xw\0\N\c7\C[B(2L) - B(L)]',
            'omegaRS2L':r'L\S\xw\0\N\c7\C[2L\xr\0)(2L) - L\xr\0(L)]',
            'std_omegaBin2L':r'\xs\0\sBin2L\N',
            'std_omegaRS2L':r'\xs\0\sRS2L\N',
            'teq':r'\xc\0\S2\N'};
    return dirLex[dirname];
            
def dirToTitle(dirname):
    dirLex = { 'en':'Energy',
            'mag':'Magnetization',
            'bin':'BinderCumulant',
            'dbdt':'dBdT',
            'xi':'Susceptibility',
            'rs':'SuperfluidDensity',
            'm2':'M2',
            'm4':'M4',
            'c':'HeatCapacity',
            'omegaBin3L':'omega_from_B',
            'omegaRS3L':'omega_from_rs',
            'omegaBin2L':'Ltoomega_from_B',
            'std_omegaBin2L':'std_intersect_Bin_vs_omega',
            'omegaRS2L':'Ltoomega_from_RS',
            'std_omegaRS2L':'std_intersect_RS_vs_omega',
            'teq':'find_teq_scaling',
            'vsN':'Equilibration_study'};
    return dirLex[dirname];
