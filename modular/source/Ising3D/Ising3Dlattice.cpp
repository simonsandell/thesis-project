#include <iostream>
#include <unistd.h>
#include <random>
#include <sys/syscall.h>

#include "Ising3Dlattice.h"
#include "Ising3Dio.h"

long double LatticeIsing3D::siteEnergy( int &s1, int &s2, int &s3){
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
long double LatticeIsing3D::calcMag(){
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

long double LatticeIsing3D::calcEn(){
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

long double *** newLatticeI3D(long double L,bool cold){
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
void LatticeIsing3D::updateQuants(){
	energy = calcEn();
	mag = calcMag();
};

//initialize new lattice
LatticeIsing3D::LatticeIsing3D(int l, bool cold,long double Beta,RandStruct r, Cluster c) 
	: rand(r), clust(c)
{
	beta = Beta;
	PROB = 1.0L - exp(-2.0L*beta);
	theLattice = newLatticeI3D((long double)l,cold);
	L = (long double)l;
	Nspins =L*L*L;
	Neqsweeps = 0.0L;
	Neqclusts = 0;
	NTotClusts = 0;
	NTotSweeps= 0.0L;
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
LatticeIsing3D::LatticeIsing3D(){

}

void LatticeIsing3D::testConsistent(){

	typedef std::numeric_limits<long double> dbl;
	std::cout.precision(dbl::max_digits10 + 5);
	long double testEn = calcEn();
	long double testMag = calcMag();
	std::cout <<std::fixed<< energy - testEn << "  E    "<< energy << " "<< testEn << std::endl;
	std::cout <<std::fixed<< mag - testMag << "  M    "<< mag << " "<< testMag << std::endl;
}
