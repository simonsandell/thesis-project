#ifndef _3DXYIO_H
#define _3DXYIO_H

#include "3DXYlattice.h"
#include "../avgStruct.h"

void printLattice3DXY(long double*** lattice,long double L);

void print3DXYOutput(Lattice3DXY & lat,long double T, avgStruct avg, long double bin, long double dbdt, long double xi, long double rs);


#endif
