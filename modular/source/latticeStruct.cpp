#include <unistd.h>
#include <random>
#include <sys/syscall.h>

#include "latticeStruct.h"
#include "ioFuncs.h"
#include "calcQuants.h"

long double*** newLattice(long double L,bool cold){
	//make new lattice
	long double ***lattice;
	lattice = new long double **[(int)L];
	for (int i = 0; i< L;++i){
		lattice[i] = new long double *[(int)L];
		for (int j =0;j<L;++j){
			lattice[i][j] = new long double[(int)L];
		}
	}

	if (cold) {
		for (int i = 0; i<L;++i){
			for (int j=0; j<L;++j){
				for (int k = 0; k<L; ++k){
					lattice[i][j][k] = 0.0L;
				}
			}
		}
	}
	else {
		//initialize rng
		unsigned long int s;
		syscall(SYS_getrandom,&s,sizeof(unsigned long int),0);	
		std::uniform_real_distribution<long double> dist(0.0L,1.0L);
		std::mt19937_64 eng; 
		eng.seed(s);
		for (int i = 0; i<L;++i){
			for (int j=0; j<L;++j){
				for (int k = 0; k<L; ++k){
					lattice[i][j][k] = dist(eng)*2.0L*M_PI;
				}
			}
		}
	}
	return lattice;
}
//update quantiites of the lattice
void Lattice::updateQuants(){
	energy = calcEn(theLattice,L);
	xmag = calcXMag(theLattice,L);
	ymag = calcYMag(theLattice,L);
	sinx = calcSinX(theLattice,L);
	siny = calcSinY(theLattice,L);
	sinz = calcSinZ(theLattice,L);
};

//initialize new lattice
Lattice::Lattice(int l, bool cold){
	theLattice = newLattice((long double)l,cold);
	L = (long double)l;
	Nspins =L*L*L;
	Neqsweeps = 0.0L;
	Neqclusts = 0;
	Nsmclusts = 0;
	Nsmsweeps = 0.0L;
	coldstart = cold;
	warmedUp = false;
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


};
Lattice::Lattice(){

}
;
