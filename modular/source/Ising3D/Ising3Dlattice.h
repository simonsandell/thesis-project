#ifndef LATTICESTRUCT_H
#define LATTICESTRUCT_H

struct LatticeIsing3D{
	long double *** theLattice;
	long double L,Nspins,Neqsweeps,NTotSweeps;
	int Neqclusts,NTotClusts;	
	bool coldstart,warmedUp;
	long double beta;

	long double energy,mag;

	long double calcEn();
	long double calcMag();

	LatticeIsing3D(int L, bool cold,long double Beta);
	LatticeIsing3D();

	void updateQuants();

	long double siteEnergy( int &s1, int &s2, int &s3);
	void testConsistent();

	long double PROB; 

	};
#endif
