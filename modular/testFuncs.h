#ifndef TESTFUNCS_H
#define TESTFUNCS_H

#include <cmath>

//print lattice
void printLattice(long double ***lattice,long double &L);

//testing functions
long double calcSinX(long double ***lattice,long double &L);
long double calcXMag(long double ***lattice,long double&L);
long double calcYMag(long double ***lattice,long double&L);
long double calcMag(long double ***lattice,long double&L);
long double calcEn(long double ***lattice,long double&L);
void testConsistent(long double ***lattice,long double&L,long double&TotEn,long double&TotXMag,long double&TotYMag,long double&TotSinX);
#endif
