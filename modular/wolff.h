#ifndef WOLFF_H
#define WOLFF_H

#include <random>
int growCluster(double ***lattice,bool ***cluster, double &L,double &beta, double& TotXMag,double& TotYMag,double& TotEn,double &TotSinX,std::uniform_real_distribution<double> &dist,std::mt19937_64 &eng);



#endif
