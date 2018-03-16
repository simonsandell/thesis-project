
def getOmegaRange(ostart,oend,step):
    omegarange = [];
    omega = ostart;
    omegarange.append(ostart);
    while (omega < oend):
        omega = omega + step;
        omegarange.append(omega);
    return omegarange;
