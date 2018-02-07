#ifndef LATTICEOPS_H
#define LATTICEOPS_H
#include <random>

void emptyCluster(bool***cluster,long double &L);
long double siteEnergy(long double *** lattice,long double &L, int &s1, int &s2, int &s3);
long double sinX(long double ***lattice,long double &L, int &s1, int &s2, int &s3,long double &angle);

long double*** newLattice(long double L,bool cold,std::uniform_real_distribution<long double> &dist,std::mt19937_64 &eng);
#endif
