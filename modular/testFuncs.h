#ifndef TESTFUNCS_H
#define TESTFUNCS_H

#include <cmath>

//print lattice
void printLattice(double ***lattice,double &L);

//testing functions
double calcSinX(double ***lattice,double &L);
double calcXMag(double ***lattice,double&L);
double calcYMag(double ***lattice,double&L);
double calcMag(double ***lattice,double&L);
double calcEn(double ***lattice,double&L);
void testConsistent(double ***lattice,double&L,double&TotEn,double&TotXMag,double&TotYMag,double&TotSinX);
#endif
