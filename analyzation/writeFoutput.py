

fs= "{:30.30f}";
def getTdict(ldict):
    tdict = {};
    for L,td in ldict.items():
        for T,af in td.items():
            if T not in tdict:
                tdict[T] = {L:af};
            else:
                tdict[T][L] = af;
    return tdict;
def writeSC3(omdicts,fName,model):
    omdictBin = omdicts[0];
    omdictRs = omdicts[1];
    for L,omlist in sorted(omdictBin.items()):
        f = open("./foutput/3DXY/scalingCorr/omegaBin3L/" + str(L) + "_"+str(fName)+".dat","w");
        for vals in omlist:
            f.write(fs.format(vals[0])+" "+fs.format(vals[1])+" 0.0\n");
    for L,omlist in sorted(omdictRs.items()):
        f = open("./foutput/3DXY/scalingCorr/omegaRS3L/" + str(L) + "_"+str(fName)+".dat","w");
        for vals in omlist:
            f.write(fs.format(vals[0])+" "+fs.format(vals[1])+" 0.0\n");
def writeSC2(omDict,fName,model):
    if (model == "3DXY"):
        omDictRS = omDict[0];
        omDictBin = omDict[1];
        for omega,sLdict in sorted(omDictRS.items()):
            for L,tlist in sorted(sLdict.items()):
                f = open("./foutput/3DXY/scalingCorr/omegaRS2L/"+str(omega)+"_"+str(L)+".dat","w");
                for vals in tlist:
                    f.write(fs.format(vals[0]) + " " + fs.format(vals[1]) + " " + fs.format(vals[2]) +"\n");
        for omega,sLdict in sorted(omDictBin.items()):
            for L,tlist in sorted(sLdict.items()):
                f = open("./foutput/3DXY/scalingCorr/omegaBin2L/"+str(omega)+"_"+str(L)+".dat","w");
                for vals in tlist:
                    f.write(fs.format(vals[0]) + " " + fs.format(vals[1]) + " " + fs.format(vals[2]) +"\n");


def writeVsT(ldict,fName,model):
    if (model == "3DXY"):
        for L,tdict in sorted(ldict.items()):
            ef = open('./foutput/3DXY/vsT/en/'+str(L)+'_'+fName+'.dat','w');
            mf = open('./foutput/3DXY/vsT/mag/'+str(L)+'_'+fName+'.dat','w');
            bf = open('./foutput/3DXY/vsT/bin/'+str(L)+'_'+fName+'.dat','w');
            df = open('./foutput/3DXY/vsT/dbdt/'+str(L)+'_'+fName+'.dat','w');
            cf = open('./foutput/3DXY/vsT/xi/'+str(L)+'_'+fName+'.dat','w');
            rf = open('./foutput/3DXY/vsT/rs/'+str(L)+'_'+fName+'.dat','w');
            for T,af in sorted(tdict.items()):
                ef.write(fs.format(T)+" "+fs.format(af.E)+ " "+fs.format(af.dE)+"\n");
                mf.write(fs.format(T)+" "+fs.format(af.M)+ " "+fs.format(af.dM)+"\n");
                bf.write(fs.format(T)+" "+fs.format(af.Bin)+ " "+fs.format(af.dBin)+"\n");
                df.write(fs.format(T)+" "+fs.format(af.dBdT)+ " "+fs.format(af.ddBdT)+"\n")
                cf.write(fs.format(T)+" "+fs.format(af.Chi)+ " "+fs.format(af.dChi)+"\n");
                rf.write(fs.format(T)+" "+fs.format(af.Rs)+" "+fs.format(af.dRs)+"\n");

def writeVsL(ldict,fName,model):
    #reverse order of dicts
    tdict = getTdict(ldict);
    if (model == "3DXY"):
        for T,ld in sorted(tdict.items()):
            ef = open('./foutput/3DXY/vsL/en/'+str(T)+'_'+fName+'.dat','w');
            mf = open('./foutput/3DXY/vsL/mag/'+str(T)+'_'+fName+'.dat','w');
            bf = open('./foutput/3DXY/vsL/bin/'+str(T)+'_'+fName+'.dat','w');
            df = open('./foutput/3DXY/vsL/dbdt/'+str(T)+'_'+fName+'.dat','w');
            cf = open('./foutput/3DXY/vsL/xi/'+str(T)+'_'+fName+'.dat','w');
            rf = open('./foutput/3DXY/vsL/rs/'+str(T)+'_'+fName+'.dat','w');
            for L,af in sorted(ld.items()):
                ef.write(fs.format(L)+" "+fs.format(af.E)+ " "+fs.format(af.dE)+"\n");
                mf.write(fs.format(L)+" "+fs.format(af.M)+ " "+fs.format(af.dM)+"\n");
                bf.write(fs.format(L)+" "+fs.format(af.Bin)+ " "+fs.format(af.dBin)+"\n");
                df.write(fs.format(L)+" "+fs.format(af.dBdT)+ " "+fs.format(af.ddBdT)+"\n")
                cf.write(fs.format(L)+" "+fs.format(af.Chi)+ " "+fs.format(af.dChi)+"\n");
                rf.write(fs.format(L)+" "+fs.format(af.Rs)+" "+fs.format(af.dRs)+"\n");
