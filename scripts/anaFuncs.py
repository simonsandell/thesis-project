
def getOmegaRange(ostart,oend,step):
    omegarange = [];
    omega = ostart;
    omegarange.append(ostart);
    while (omega < oend):
        omega = omega + step;
        omegarange.append(omega);
    return omegarange;

def dirToYaxis(dirname):
    dirLex = { 'en':r'<e> Energy per spin',
            'mag':r'<m> Magnetization per spin',
            'bin':r'B = <M\S4\N>/<M\S2\N>\S2\N',
            'dbdt':r'dB/dT',
            'xi':r'\xc\0 Susceptibility',
            'rs':r'L\xr\0\ss\N Superfluid density',
            'm2':r'<m\S2\N>',
            'm4':r'<m\S4\N>',
            'c':'C - Heat Capacity',
            'omegaBin3L':r'\xw\0 B scaling correction',
            'omegaRS3L':r'\xw\0 \xr\0\ss\N scaling correctoin',
            'omegaBin2L':r'L\S\xw\0\N\c7\C[B(2L) - B(L)]',
            'omegaRS2L':r'L\S\xw\0\N\c7\C[2L\c7\C\xr\0\ss\N(2L) - \L\c7\C\xr\0\ss\N(L)]'};
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
            'omegaRS2L':'Ltoomega_from_RS'};
    return dirLex[dirname];
