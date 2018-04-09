#ifndef IOFUNCS_H
#define IOFUNCS_H

#include "Ising3Dlattice.h"
#include "../avgStruct.h"
void printIsing3DOutput(LatticeIsing3D &lat,long double T, avgStruct avg, long double bin, long double dbdt, long double xi, long double rs);

void saveLatticeIsing3D(LatticeIsing3D &lat);

LatticeIsing3D getLattice(int l);



#endif
