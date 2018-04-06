#ifndef _3DXY_H
#define _3DXY_H
#include "3DXY/3DXYlattice.h"
#include "clusterStruct.h"
#include "randStruct.h"
namespace _3DXY {

void warmup(Lattice3DXY& lat,long double N);

void wolffHistJob(long double L);
void teqRun(long double L,bool cold);

};




#endif
