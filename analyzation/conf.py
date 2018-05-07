import collections
model = "3DXY"
jackknife_on = 0;
jackknife_blocks= 1;

MCAvg = '';
avgF = '';
quantStruct = '';

def setModel(m):
    global model;
    model = m;

def setJackknifeBlock(n):
    if (n == 0):
        setJackknifeOn(False);
    else:
        setJackknifeOn(True);
    global jackknife_blocks;
    jackknife_blocks = n;
def setJackknifeOn(b):
    global jackknife_on;
    jackknife_on = b;

def initNT():
    global MCAvg;
    global avgF;
    global quantStruct;
    if (model == "3DXY"):
        quantStruct = collections.namedtuple('quantStruct',['Bin','Rs']); 
        avgF = collections.namedtuple('avgF',['E','M','Bin','dBdT','Chi','Rs','C','dE',  'dM','dBin','ddBdT','dChi','dRs','dC']);
        MCAvg = collections.namedtuple('MCAvg',['L','T','Neqsw','Neqcl','NTotsw','NTotcl','cold','e','e2','m','m2','m4','m2e','m4e','s2x','s2y','s2z','bin','dbdt','chi','rs','expFac']);

