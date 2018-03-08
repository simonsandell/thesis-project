#include <iostream>
#include <unistd.h>
#include <random>
#include <sys/syscall.h>

#include "latticeStruct.h"
#include "ioFuncs.h"

long double Lattice::siteEnergy( int &s1, int &s2, int &s3){
	long double sum = 0.0L;
	//find indices of neighbours
	int n1m = (s1 -1 + (int)L )%(int)L;
	int n1p = (s1 +1 + (int)L )%(int)L;
	int n2m = (s2 -1 + (int)L )%(int)L;
	int n2p = (s2 +1 + (int)L )%(int)L;
	int n3m = (s3 -1 + (int)L )%(int)L;
	int n3p = (s3 +1 + (int)L )%(int)L;
	//sum 
	sum -= theLattice[s1][s2][s3]*theLattice[n1m][s2][s3];
	sum -= theLattice[s1][s2][s3]*theLattice[n1p][s2][s3];
	sum -= theLattice[s1][s2][s3]*theLattice[s1][n2m][s3];
	sum -= theLattice[s1][s2][s3]*theLattice[s1][n2p][s3];
	sum -= theLattice[s1][s2][s3]*theLattice[s1][s2][n3m];
	sum -= theLattice[s1][s2][s3]*theLattice[s1][s2][n3p];
	return sum;
}
//calculate sin(theta - theta_x) upwards +, downward -
long double Lattice::calcMag(){
	long double ret = 0.0L;
	for (int i = 0; i<L; ++i){
		for (int j = 0; j<L; ++j){
			for (int k = 0; k<L; ++k){
				ret += theLattice[i][j][k];
			}
		}
	}
	return ret;
}

long double Lattice::calcEn(){
	long double en = 0.0L;
	for (int i = 0; i< L; ++i){
		for (int j = 0; j< L; ++j){
			for (int k = 0; k<L; ++k){	
				en += siteEnergy(i,j,k);
			}
		}
	}
	en *= 0.5L;
	return en;
}

long double *** newLattice(long double L,bool cold){
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
					lattice[i][j][k] = 1.0L;
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
					if ( dist(eng) >0.5L){
						lattice[i][j][k] =1.0L;
					}
					else {
						lattice[i][j][k] =-1.0L;
					}
				}
			}
		}
	}
	return lattice;
}
//update quantiites of the lattice
void Lattice::updateQuants(){
	energy = calcEn();
	mag = calcMag();
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
		mag = Nspins;
	}
	else {
		energy = calcEn();
		mag = calcMag();
	}


};
Lattice::Lattice(){

}

void Lattice::testConsistent(){

	typedef std::numeric_limits<long double> dbl;
	std::cout.precision(dbl::max_digits10 + 5);
	long double testEn = calcEn();
	long double testMag = calcMag();
	std::cout <<std::fixed<< energy - testEn << "  E    "<< energy << " "<< testEn << std::endl;
	std::cout <<std::fixed<< mag - testMag << "  M    "<< mag << " "<< testMag << std::endl;
}
