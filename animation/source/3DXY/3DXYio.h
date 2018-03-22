#ifndef _3DXYIO_H
#define _3DXYIO_H

#include "3DXYlattice.h"
#include "../avgStruct.h"
void printLattice3DXY(long double***lattice,long double L);
void print3DXYOutput(Lattice3DXY lat,long double T, avgStruct avg, long double bin, long double dbdt, long double xi, long double rs);

long double getMaxE3DXY(long double L);

void setMaxE3DXY(long double L,long double newE);

void saveLattice3DXY(Lattice3DXY lat);

Lattice3DXY getLattice3DXY(int l);



#endif
