#ifndef METROPOLIS_H
#define METROPOLIS_H
#include <random>
void metrosweep(long double***lattice,long double&L,long double&beta,long double&TotXMag,long double&TotYMag,long double&TotEn,long double &TotSinX,long double &TotSinY,long double &TotSinZ,std::uniform_real_distribution<long double> &dist,std::mt19937_64 &eng);
#endif
