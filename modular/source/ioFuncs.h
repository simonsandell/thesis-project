#ifndef IOFUNCS_H
#define IOFUNCS_H

#include "latticeStruct.h"
void printOutput(Lattice lat, long double T, long double E, long double E2, long double M, long double M2, long double M4, long double M2E, long double M4E, long double SX2, long double SY2, long double SZ2, long double bin, long double dbdt, long double xi, long double rs, long double expFac);

long double getMaxE(long double L);

void setMaxE(long double L,long double newE);

void saveLattice(Lattice lat);

Lattice getLattice(int l);



#endif
