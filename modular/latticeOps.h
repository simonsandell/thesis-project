#ifndef LATTICEOPS_H
#define LATTICEOPS_H
#include <random>

void emptyCluster(bool***cluster,double &L);
double siteEnergy(double *** lattice,double &L, int &s1, int &s2, int &s3);
double sinX(double ***lattice,double &L, int &s1, int &s2, int &s3,double &angle);

double*** newLattice(double L,bool cold,std::uniform_real_distribution<double> &dist,std::mt19937_64 &eng);
#endif
