model =''
jackknife_on = 0;
jackknife_blocks= 1;
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

