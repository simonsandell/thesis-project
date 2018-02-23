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

	};
#endif
