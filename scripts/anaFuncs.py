
def dirToXaxis(fullpath):
    if ('vsT' in fullpath):
        return "Temperature";
    if ('vsL' in fullpath):
        return "L";
    if ('vsO' in fullpath):
        return "Omega";
    if ('vsN' in fullpath):
        return r"N\ssweeps\S";
    if ('findZ' in fullpath):
        return "z";
    if ('scalingCorr' in fullpath):
        return "Temperature";
    if ('intersections' in fullpath):
        return "1/L";
    else:
        return "unknown"

def dirToYaxis(dirname):
    dirLex = { 'en':r'e Energy per spin',
            'mag':r'm Magnetization per spin',
            'bin':r'B = M\S4\N/M\S2\N',
            'dbdt':r'dB/dT',
            'chi':r'\xc\0 Susceptibility',
            'rs':r'L\xr\0\ss\N Superfluid density',
            'm2':r'm\S2\N',
            'm4':r'm\S4\N',
            'c':'C - Heat Capacity',
            'teq':'Magnetization',
            'omegaBin3L':r'\xw\0 = -ln(B(4L) - B(2L)/B(2L) - B(L))/ln(2)',
            'omegaRS3L':r'\xw\0 = -ln(\xr\0\ss\N(4L) - \xr\0\ss\N(2L)/\xr\0\ss\N(2L) - \xr\0\ss\N(L))/ln(2)',
            'omegaBin2L':r'L\S\xw\0\N\c7\C[B(2L) - B(L)]',
            'omegaRS2L':r'L\S\xw\0\N\c7\C[2L\xr\0)(2L) - L\xr\0(L)]',
            'std_omegaBin2L':r'\xs\0\sBin2L\N',
            'std_omegaRS2L':r'\xs\0\sRS2L\N',
            'sigmaVsZ':r'\xc\0\S2\N'};

    if dirname in dirLex:
        return dirLex[dirname];
    else:
        return "unknown"
            
def dirToTitle(dirname):
    dirLex = { 'en':'Energy',
            'mag':'Magnetization',
            'bin':'BinderCumulant',
            'dbdt':'dBdT',
            'chi':'Susceptibility',
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
            'sigmaVsZ':'find_teq_scaling',
            'teq':'Equilibration_study'};
    if dirname in dirLex:
        return dirLex[dirname];
    else:
        return "unknown"

def dirToLogPlot(fullpath):
    if ('vsT' in fullpath):
        return [False,False];
    if ('vsL' in fullpath):
        return [True,True];
    if ('vsN' in fullpath):
        return [True,False];
    if ('teq' in fullpath):
        return [False,False];
    if ('scalingCorr' in fullpath):
        return [False,False];
    return [False,False];

def getParams(dirname,fullpath,doPrint):
    title = dirToTitle(dirname);
    xaxis = dirToXaxis(fullpath);
    yaxis = dirToYaxis(dirname);
    [xlog,ylog] = dirToLogPlot(fullpath);
    return [fullpath,title,xaxis,yaxis,xlog,ylog,doPrint];

def get3DXYIndex():
    res = {"L":0   ,
           "T":1    ,
           "eqsw":2 ,
           "eqcl":3 ,
           "totsw":4,
           "totcl":5,
           "cold":6 ,
           "e":7    ,
           "e2":8   ,
           "m":9    ,
           "m2":10  ,
           "m4":11  ,
           "m2e":12 ,
           "m4e":13 ,
           "s2x":14 ,
           "s2y":15 ,
           "s2z":16 ,
           "b":[17,"bin"],
           "dbdt":[18,"dbdt"],
           "chi":[19,"chi"] ,
           "rs":[20,"rs"]  ,
           "expF":21,
           "B":[22,"bin"]   ,
           "C":[23,"c"]   ,
           "CHI":[24,"chi"] ,
           "DBDT":[25,"dbdt"],
           "RS":[26,"rs"]  ,
           "EN":[27,"en"]  ,
           "MAG":[28,"mag"] ,
           "Nmcavg":29,
           "last":30};
    return res;
