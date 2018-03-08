#ifndef METROPOLIS_H
#define METROPOLIS_H
#include <random>

#include "latticeStruct.h"
#include "randStruct.h"
void metrosweep(Lattice& lat,long double beta,RandStruct randgen);
#endif
