#ifndef LATTICESTRUCT_H
#define LATTICESTRUCT_H

struct Lattice{
	long double *** theLattice;
	long double L,Nspins,Neqsweeps,Nsmsweeps;
	int Neqclusts,Nsmclusts;	
	bool coldstart,warmedUp;

	long double energy,xmag,ymag,sinx,siny,sinz;

	Lattice(int L, bool cold);
	Lattice();

	void updateQuants();

	long double siteEnergy(Lattice lat, int &s1, int &s2, int &s3);
	long double sinX(Lattice lat, int &s1, int &s2, int &s3,long double &angle);
	long double sinY(Lattice lat, int &s1, int &s2, int &s3,long double &angle);
	long double sinZ(Lattice lat, int &s1, int &s2, int &s3,long double &angle);


	};
#endif
