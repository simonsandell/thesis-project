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
	sum -= theLattice[s1][s2][s3]-theLattice[n1m][s2][s3];
	sum -= theLattice[s1][s2][s3]-theLattice[n1p][s2][s3];
	sum -= theLattice[s1][s2][s3]-theLattice[s1][n2m][s3];
	sum -= theLattice[s1][s2][s3]-theLattice[s1][n2p][s3];
	sum -= theLattice[s1][s2][s3]-theLattice[s1][s2][n3m];
	sum -= theLattice[s1][s2][s3]-theLattice[s1][s2][n3p];
	return sum;
}
//calculate sin(theta - theta_x) upwards +, downward -
long double calcMag(long double ***lattice,long double L){
	long double ret = 0.0L;
	for (int i = 0; i<L; ++i){
		for (int j = 0; j<L; ++j){
			for (int k = 0; k<L; ++k){
				ret += lattice[i][j][k];
			}
		}
	}
	return ret;
}

long double calcEn(Lattice* lat){
	long double en = 0.0L;
	for (int i = 0; i< lat->L; ++i){
		for (int j = 0; j< lat->L; ++j){
			for (int k = 0; k<lat->L; ++k){	
				en += lat->siteEnergy(i,j,k);
			}
		}
	}
	en = 0.5L*en;
	return en;
}
long double*** newLattice(long double L,bool cold){
	//make new lattice
	int ***lattice;
	lattice = new int**[(int)L];
	for (int i = 0; i< L;++i){
		lattice[i] = new int*[(int)L];
		for (int j =0;j<L;++j){
			lattice[i][j] = new int[(int)L];
		}
	}

	if (cold) {
		for (int i = 0; i<L;++i){
			for (int j=0; j<L;++j){
				for (int k = 0; k<L; ++k){
					lattice[i][j][k] = 1;
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
						lattice[i][j][k] =1;
					}
					else {
						lattice[i][j][k] =-1;
					}
				}
			}
		}
	}
	return lattice;
}
//update quantiites of the lattice
void Lattice::updateQuants(){
	energy = calcEn(this);
	mag = calcMag(theLattice,L);
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
		mag = Nspins;
		sinx = 0.0L;
		siny = 0.0L;
		sinz = 0.0L;
	}
	else {
		energy = calcEn(this);
		mag = calcMag(theLattice,L);
		sinx = calcSinX(theLattice,L);
		siny = calcSinY(theLattice,L);
		sinz = calcSinZ(theLattice,L);
	}


};
Lattice::Lattice(){

}

void Lattice::testConsistent(){

	typedef std::numeric_limits<long double> dbl;
	std::cout.precision(dbl::max_digits10 + 5);
	long double testSinX = calcSinX(theLattice,L);
	long double testSinY = calcSinY(theLattice,L);
	long double testSinZ = calcSinZ(theLattice,L);
	long double testEn = calcEn(this);
	long double testMag = calcMag(theLattice,L);
	long double TotEn = energy;
	long double TotXMag= xmag;
	long double TotYMag= ymag;
	long double TotSinX= sinx;
	long double TotSinY = siny;
	long double TotSinZ = sinz;
	std::cout <<std::fixed<< TotEn - testEn << "  E    "<< TotEn << " "<< testEn << std::endl;
	std::cout <<std::fixed<< TotMag - testMag << "  M    "<< TotMag << " "<< testMag << std::endl;
}
