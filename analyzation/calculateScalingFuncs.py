import numpy as np
import math
def calcSC3(tdict,model):
    if (model == "3DXY"):
        omDictBin = {};
        omDictRs = {};
        for T,ldict in sorted(tdict.items()):
            Llist = sorted(list(ldict.keys()));
            print(Llist);
            if (len(Llist)>2):
                Llist1 = Llist[:len(Llist)-2];
                Llist2 = Llist[1:len(Llist)-1];
                Llist3 = Llist[2:];

                for L1,L2,L3 in zip(Llist1,Llist2,Llist3):
                    print([L1,L2,L3])
                    if (not L1*2 == L2 or not L2*2==L3):
                        print('calcSC3: L not powers of 2');
                    omegaBin = - np.log((ldict[L3].Bin - ldict[L2].Bin)/(ldict[L2].Bin - ldict[L1].Bin))/np.log(2);
                    if L1 not in omDictBin:
                        omDictBin[L1] = [[T,omegaBin]];
                    else:

                        omDictBin[L1].append([T,omegaBin]);
                    
                    omegaRs = -np.log((ldict[L3].Rs - ldict[L2].Rs)/(ldict[L2].Rs - ldict[L1].Rs))/np.log(2);
                    if L1 not in omDictRs:
                        if not (math.isnan(T)):
                            omDictRs[L1] = [[T,omegaRs]];
                    else:
                        if not (math.isnan(T)):
                            omDictRs[L1].append([T,omegaRs]);
        return [omDictBin,omDictRs];

def calcSC2(tdict,model):
    if (model == "3DXY"):
        omDictRS = {}
        omDictBin = {}
        O = 0
        dO = 0.05;
        orange = [];
        while (O < (1.5+dO)):
            orange.append(O);
            omDictRS[O] = {};
            omDictBin[O] = {};
            O = O+dO;
        for T,ldict in sorted(tdict.items()):
            Llist = sorted(list(ldict.keys()));
            Llist1 = Llist[:len(Llist)-1];
            Llist2 = Llist[1:];
            for L1,L2 in zip(Llist1,Llist2):
                for omega in orange:
                    quantRS=  pow(L1,omega)*(ldict[L2].Rs - ldict[L1].Rs);
                    deltaRS = pow(L1,omega)*pow(pow(ldict[L2].dRs,2) + pow(ldict[L1].dRs,2),0.5);
                    quantBin=  pow(L1,omega)*(ldict[L2].Bin - ldict[L1].Bin);
                    deltaBin = pow(L1,omega)*pow(pow(ldict[L2].dBin,2) + pow(ldict[L1].dBin,2),0.5);
                    if L1 not in omDictRS[omega]:
                        omDictRS[omega][L1] = [[T,quantRS,deltaRS]];
                        omDictBin[omega][L1] = [[T,quantBin,deltaBin]];
                    else:
                        omDictRS[omega][L1].append([T,quantRS,deltaRS]);
                        omDictBin[omega][L1].append([T,quantBin,deltaBin]);
        ret = [omDictRS,omDictBin];
        return ret;
    
