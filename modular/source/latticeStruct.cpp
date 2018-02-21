#include <unistd.h>
#include <random>
#include <sys/syscall.h>
struct Lattice {

	long double *** theLattice;
	long double L,Nspins,Neqsweeps,Nsmsweeps;
	int Neqclusts,Nsmclusts;	


	Lattice(int l, bool cold){
		long double *** theLattice;
		long double L = (long double)l,Nspins =0,Neqsweeps=0,Nsmsweeps=0;
		int Neqclusts=0,Nsmclusts=0;	

		theLattice = new long double**[l];
		for (int i = 0; i < l; ++i){
			theLattice[i] = new long double *[l];
			for (int j = 0; j < l; ++j){
				theLattice[i][j] = new long double[l];	
			}
		}
		if (cold){
			for (int i = 0; i<l; ++i){
				for (int j = 0; j<l; ++j){
					for (int k = 0; k<l; ++k){
						theLattice[i][j][k] = 0.0L;
					}}}
		}
		else {
			unsigned long int s;
			syscall(SYS_getrandom,&s,sizeof(unsigned long int),0);	
			std::uniform_real_distribution<long double> dist(0.0L,1.0L);
			std::mt19937_64 eng; 
			eng.seed(s);
			for (int i = 0; i<l;++i){
				for (int j=0; j<l;++j){
					for (int k = 0; k<l; ++k){
						theLattice[i][j][k] =
							-(long double)M_PI+ 
							dist(eng)*2.0L*(long double)M_PI;
					}
				}
			}

		}
	}
	Lattice(int l){
		long double *** theLattice;
		long double L = (long double)l,Nspins =0,Neqsweeps=0,Nsmsweeps=0;
		int Neqclusts=0,Nsmclusts=0;	
		theLattice = new long double**[l];
		for (int i = 0; i < l; ++i){
			theLattice[i] = new long double *[l];
			for (int j = 0; j < l; ++j){
				theLattice[i][j] = new long double[l];	
			}
		}

	}
};
