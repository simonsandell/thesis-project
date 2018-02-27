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
long double Lattice::siteEnergy(Lattice lat, int &s1, int &s2, int &s3){
	long double sum = 0.0L;
	//find indices of neighbours
	int n1m = (s1 -1 + (int)L )%(int)L;
	int n1p = (s1 +1 + (int)L )%(int)L;
	int n2m = (s2 -1 + (int)L )%(int)L;
	int n2p = (s2 +1 + (int)L )%(int)L;
	int n3m = (s3 -1 + (int)L )%(int)L;
	int n3p = (s3 +1 + (int)L )%(int)L;
	sum -= cos(lat.theLattice[s1][s2][s3]-lat.theLattice[n1m][s2][s3]);
	sum -= cos(lat.theLattice[s1][s2][s3]-lat.theLattice[n1p][s2][s3]);
	sum -= cos(lat.theLattice[s1][s2][s3]-lat.theLattice[s1][n2m][s3]);
	sum -= cos(lat.theLattice[s1][s2][s3]-lat.theLattice[s1][n2p][s3]);
	sum -= cos(lat.theLattice[s1][s2][s3]-lat.theLattice[s1][s2][n3m]);
	sum -= cos(lat.theLattice[s1][s2][s3]-lat.theLattice[s1][s2][n3p]);
	return sum;
}
//calculate sin(theta - theta_x) upwards +, downward -
long double Lattice::sinX(Lattice lat, int &s1, int &s2, int &s3,long double &angle){
	int np = (s1 + 1) %(int)L;
	int nm = (s1 -1 + (int)L) % (int)L;	
	long double ret = 0.0L;
	ret = sin(lat.theLattice[nm][s2][s3] - angle) + sin(angle - lat.theLattice[np][s2][s3]);
	return ret;
}
long double Lattice::sinY(Lattice lat, int &s1, int &s2, int &s3,long double &angle){
	int np = (s2 + 1) %(int)L;
	int nm = (s2 -1 + (int)L) % (int)L;	
	long double ret = 0.0L;
	ret = sin(lat.theLattice[s1][nm][s3] - angle) + sin(angle - lat.theLattice[s1][np][s3]);
	return ret;
}
long double Lattice::sinZ(Lattice lat, int &s1, int &s2, int &s3,long double &angle){
	int np = (s3 + 1) %(int)L;
	int nm = (s3 -1 + (int)L) % (int)L;	
	long double ret = 0.0L;
	ret = sin(lat.theLattice[s1][s2][nm] - angle) + sin(angle - lat.theLattice[s1][s2][np]);
	return ret;
}
;
