#ifndef LATTICEOPS_H
#define LATTICEOPS_H




void emptyCluster(bool***cluster,double &L);
double siteEnergy(double *** lattice,double &L, int &s1, int &s2, int &s3);
double sinX(double ***lattice,double &L, int &s1, int &s2, int &s3,double &angle);

#endif
