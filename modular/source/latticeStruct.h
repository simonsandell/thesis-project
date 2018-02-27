#ifndef LATTICESTRUCT_H
#define LATTICESTRUCT_H

struct Lattice{
	long double *** theLattice;
	long double L,Nspins,Neqsweeps,Nsmsweeps;
	int Neqclusts,Nsmclusts;	
	bool coldstart,warmedUp;

	long double energy,mag;

	long double calcEn();
	long double calcMag();

	Lattice(int L, bool cold);
	Lattice();

	void updateQuants();

	long double siteEnergy( int &s1, int &s2, int &s3);
	void testConsistent();

	};
#endif
