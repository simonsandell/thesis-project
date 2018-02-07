#ifndef WOLFF_H
#define WOLFF_H

#include <random>
int growCluster(long double ***lattice,bool ***cluster, long double &L,long double &beta, long double& TotXMag,long double& TotYMag,long double& TotEn,long double &TotSinX,long double &TotSinY,long double &TotSinZ,std::uniform_real_distribution<long double> &dist,std::mt19937_64 &eng);



#endif
