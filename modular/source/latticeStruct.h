#ifndef LATTICESTRUCT_H
#define LATTICESTRUCT_H

struct Lattice{
	long double *** theLattice;
	long double L,Nspins,Neqsweeps,Nsmsweeps;
	int Neqclusts,Nsmclusts;	

	Lattice(int L, bool cold){};
	Lattice(int L){};

	};
#endif
