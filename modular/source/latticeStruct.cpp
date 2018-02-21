#include <unistd.h>
#include <random>
#include <sys/syscall.h>
struct Lattice {

	long double *** theLattice;
	long double L,Nspins,Neqsweeps,Nsmsweeps;
	int Neqclusts,Nsmclusts;	

	long double energy,xmag,ymag,sinx,siny,sinz;


	//initialize new lattice
	Lattice(int l, bool cold){
		long double *** theLattice = newLattice((long double)l,cold);
		L = (long double)l;
		Nspins =L*L*L;
		Neqsweeps = 0.0L;
		Neqclusts = 0;
		Nsmclusts = 0;
		Nsmsweeps = 0.0L;
		if (cold) {
			energy = -3.0L*Nspins;
			xmag = Nspins;
			ymag = 0.0L;
			sinx = 0.0L;
			siny = 0.0L;
			sinz = 0.0L;
		}
		else {
			energy = calcEn(theLattice,L);
			xmag = calcEn(theLattice,L);
			ymag = calcYMag(theLattice,L); 
			sinx = calcSinX(theLattice,L);
			siny = calcSinY(theLattice,L);
			sinz = calcSinZ(theLattice,L);
		}


	}
	//load lattice from file
	Lattice(int l){

		long double *** theLattice;
	}
};
