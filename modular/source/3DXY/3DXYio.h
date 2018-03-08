#ifndef 3DXYIO_H
#define 3DXYIO_H

#include "3DXYlattice.h"
#include "avgStruct.h"
void printOutput(Lattice lat,long double T, avgStruct avg, long double bin, long double dbdt, long double xi, long double rs);

long double getMaxE(long double L);

void setMaxE(long double L,long double newE);

void saveLattice(Lattice lat);

Lattice getLattice(int l);



#endif
