import conf
import math

fs= "{:30.30f}";
def writeBinInt(blist,fName):
    fb = open('./foutput/3DXY/intersections/bin/T_int_vs_reciL' +fName +'.dat',"w");
    for ln in blist:
        fb.write(fs.format(ln[0])+" "+fs.format(ln[1])+" 0.0 "+fs.format(ln[2])+" \n");
def writeDenInt(dlist,fName):
    fr = open('./foutput/3DXY/intersections/rs/T_int_vs_reciL' +fName +'.dat',"w");
    for ln in dlist:
        fr.write(fs.format(ln[0])+" "+fs.format(ln[1])+" 0.0 "+fs.format(ln[2])+" \n");


def writeSigmaVsOmega(sigmalist,fName):
    fb = open('./foutput/3DXY/scalingCorr/std_omegaBin2L/sigmaVsOmega_'+fName+".dat",'w');
    fr = open('./foutput/3DXY/scalingCorr/std_omegaRS2L/sigmaVsOmega_'+fName+".dat",'w');
    for ln in sigmalist.Bin:
        print(ln)
        fb.write(fs.format(ln[0]) + " " + fs.format(ln[1]) +" 0.0 " + fs.format(ln[2])+ " \n");
    for ln in sigmalist.Rs:
        fr.write(fs.format(ln[0]) + " " + fs.format(ln[1]) +" 0.0 " + fs.format(ln[2])+ " \n");


def writeSC3(omdicts,fName):
    filedictBin ={};
    filedictRs ={};
    for T,omstruct in omdicts.items():
        for L,val in omstruct.Bin.items():
            if not (math.isnan(val[1])):
                if not L in filedictBin:
                    filedictBin[L] = open(
                            './foutput/3DXY/scalingCorr/omegaBin3L/'+str(L)
                            +'_'+fName+'.dat','w');
                if not (math.isnan(val[1])):
                    filedictBin[L].write(fs.format(val[0])
                            +" "+fs.format(val[1])+" "+fs.format(val[2])
                            +" "+fs.format(val[3])+" "+fs.format(val[4])
                            +" "+fs.format(val[5])+" "+fs.format(val[6])+" \n");
        if (conf.model == '3DXY'):
            for L,val in omstruct.Rs.items():
                if not (math.isnan(val[1])):
                    if not L in filedictRs:
                        filedictRs[L] = open(
                                './foutput/3DXY/scalingCorr/omegaRS3L/'+str(L)
                                +'_'+fName+'.dat','w');
                    if not (math.isnan(val[1])):
                        filedictRs[L].write(fs.format(val[0])
                                +" "+fs.format(val[1])+" "+fs.format(val[2])
                                +" "+fs.format(val[3])+" "+fs.format(val[4])
                                +" "+fs.format(val[5])+" "+fs.format(val[6])+" \n");

def writeSC2(tlist,fName):
    filedictBin ={};
    filedictRs ={};
    for omstruct in tlist:
        for omega,vlist in omstruct.Bin.items():
            L = vlist[4];
            if not L in filedictBin:
                filedictBin[L] = open('./foutput/3DXY/scalingCorr/omegaBin2L/'
                        +str(omega)+"_"+str(L)+".dat","w");
            filedictBin[L].write(fs.format(vlist[0])+" "
                    +fs.format(vlist[1])+" "+fs.format(vlist[2])+" "
                    +fs.format(vlist[3])+" "+fs.format(vlist[4])+" "
                    +fs.format(vlist[5])+" \n");
        if (conf.model == "3DXY"):
            for omega,vlist in omstruct.Rs.items():
                L = vlist[4];
                if not L in filedictRs:
                    filedictRs[L] = open('./foutput/3DXY/scalingCorr/omegaRS2L/'
                            +str(omega)+"_"+str(L)+".dat","w");
                filedictRs[L].write(fs.format(vlist[0])+" "
                        +fs.format(vlist[1])+" "+fs.format(vlist[2])+" "
                        +fs.format(vlist[3])+" "+fs.format(vlist[4])+" "
                        +fs.format(vlist[5])+" \n");


def writeVsT(ldict,fName):
    if (conf.model == "3DXY"):
        for L,tdict in sorted(ldict.items()):
            ef = open('./foutput/3DXY/vsT/en/'+str(L)+'_'+fName+'.dat','w');
            mf = open('./foutput/3DXY/vsT/mag/'+str(L)+'_'+fName+'.dat','w');
            bf = open('./foutput/3DXY/vsT/bin/'+str(L)+'_'+fName+'.dat','w');
            df = open('./foutput/3DXY/vsT/dbdt/'+str(L)+'_'+fName+'.dat','w');
            cf = open('./foutput/3DXY/vsT/xi/'+str(L)+'_'+fName+'.dat','w');
            rf = open('./foutput/3DXY/vsT/rs/'+str(L)+'_'+fName+'.dat','w');
            for T,af in sorted(tdict.items()):
                ef.write(fs.format(T)+" "+fs.format(af.E)+ " "+fs.format(af.dE)+" \n");
                mf.write(fs.format(T)+" "+fs.format(af.M)+ " "+fs.format(af.dM)+" \n");
                bf.write(fs.format(T)+" "+fs.format(af.Bin)+ " "+fs.format(af.dBin)+" \n");
                df.write(fs.format(T)+" "+fs.format(af.dBdT)+ " "+fs.format(af.ddBdT)+" \n")
                cf.write(fs.format(T)+" "+fs.format(af.Chi)+ " "+fs.format(af.dChi)+" \n");
                rf.write(fs.format(T)+" "+fs.format(af.Rs)+" "+fs.format(af.dRs)+" \n");

def writeVsL(tdict,fName):
    #reverse order of dicts
    if (conf.model == "3DXY"):
        for T,ld in sorted(tdict.items()):
            ef = open('./foutput/3DXY/vsL/en/'+str(T)+'_'+fName+'.dat','w');
            mf = open('./foutput/3DXY/vsL/mag/'+str(T)+'_'+fName+'.dat','w');
            bf = open('./foutput/3DXY/vsL/bin/'+str(T)+'_'+fName+'.dat','w');
            df = open('./foutput/3DXY/vsL/dbdt/'+str(T)+'_'+fName+'.dat','w');
            cf = open('./foutput/3DXY/vsL/xi/'+str(T)+'_'+fName+'.dat','w');
            rf = open('./foutput/3DXY/vsL/rs/'+str(T)+'_'+fName+'.dat','w');
            for L,af in sorted(ld.items()):
                ef.write(fs.format(L)+" "+fs.format(abs(af.E))+" "+fs.format(af.dE)+" \n");
                mf.write(fs.format(L)+" "+fs.format(abs(af.M))+" "+fs.format(af.dM)+" \n");
                bf.write(fs.format(L)+" "+fs.format(abs(af.Bin))+" "+fs.format(af.dBin)+" \n");
                df.write(fs.format(L)+" "+fs.format(abs(af.dBdT))+" "+fs.format(af.ddBdT)+" \n")
                cf.write(fs.format(L)+" "+fs.format(abs(af.Chi))+" "+fs.format(af.dChi)+" \n");
                rf.write(fs.format(L)+" "+fs.format(abs(af.Rs))+" "+fs.format(af.dRs)+" \n");

def writeVsTAlt(ldict,fName):
    if (conf.model == "3DXY"):
        for L,tdict in sorted(ldict.items()):
            bf = open('./foutput/3DXY/vsT/bin/'+str(L)+'_'+fName+'.dat','w');
            df = open('./foutput/3DXY/vsT/dbdt/'+str(L)+'_'+fName+'.dat','w');
            cf = open('./foutput/3DXY/vsT/xi/'+str(L)+'_'+fName+'.dat','w');
            rf = open('./foutput/3DXY/vsT/rs/'+str(L)+'_'+fName+'.dat','w');
            for T,af in sorted(tdict.items()):
                bf.write(fs.format(T)+" "+fs.format(af.Bin)+ " "+fs.format(af.dBin)+" \n");
                df.write(fs.format(T)+" "+fs.format(af.dBdT)+ " "+fs.format(af.ddBdT)+" \n")
                cf.write(fs.format(T)+" "+fs.format(af.Chi)+ " "+fs.format(af.dChi)+" \n");
                rf.write(fs.format(T)+" "+fs.format(af.Rs)+" "+fs.format(af.dRs)+" \n");

def writeVsLAlt(tdict,fName):
    #reverse order of dicts
    if (conf.model == "3DXY"):
        for T,ld in sorted(tdict.items()):
            bf = open('./foutput/3DXY/vsL/bin/'+str(T)+'_'+fName+'.dat','w');
            df = open('./foutput/3DXY/vsL/dbdt/'+str(T)+'_'+fName+'.dat','w');
            cf = open('./foutput/3DXY/vsL/xi/'+str(T)+'_'+fName+'.dat','w');
            rf = open('./foutput/3DXY/vsL/rs/'+str(T)+'_'+fName+'.dat','w');
            for L,af in sorted(ld.items()):
                bf.write(fs.format(L)+" "+fs.format(abs(af.Bin))+" "+fs.format(af.dBin)+" \n");
                df.write(fs.format(L)+" "+fs.format(abs(af.dBdT))+" "+fs.format(af.ddBdT)+" \n")
                cf.write(fs.format(L)+" "+fs.format(abs(af.Chi))+" "+fs.format(af.dChi)+" \n");
                rf.write(fs.format(L)+" "+fs.format(abs(af.Rs))+" "+fs.format(af.dRs)+" \n");
