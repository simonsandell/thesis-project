#include <iostream>
#include <unistd.h>
#include <random>
#include <sys/syscall.h>

#include "3DXYlattice.h"
#include "3DXYio.h"

long double Lattice3DXY::siteEnergy( int &s1, int &s2, int &s3){
	long double sum = 0.0L;
	//find indices of neighbours
	int n1m = (s1 -1 + (int)L )%(int)L;
	int n1p = (s1 +1 + (int)L )%(int)L;
	int n2m = (s2 -1 + (int)L )%(int)L;
	int n2p = (s2 +1 + (int)L )%(int)L;
	int n3m = (s3 -1 + (int)L )%(int)L;
	int n3p = (s3 +1 + (int)L )%(int)L;
	sum -= cos(theLattice[s1][s2][s3]-theLattice[n1m][s2][s3]);
	sum -= cos(theLattice[s1][s2][s3]-theLattice[n1p][s2][s3]);
	sum -= cos(theLattice[s1][s2][s3]-theLattice[s1][n2m][s3]);
	sum -= cos(theLattice[s1][s2][s3]-theLattice[s1][n2p][s3]);
	sum -= cos(theLattice[s1][s2][s3]-theLattice[s1][s2][n3m]);
	sum -= cos(theLattice[s1][s2][s3]-theLattice[s1][s2][n3p]);
	return sum;
}
//calculate sin(theta - theta_x) upwards +, downward -
long double Lattice3DXY::sinX(int &s1, int &s2, int &s3,long double &angle){
	int np = (s1 + 1) %(int)L;
	int nm = (s1 -1 + (int)L) % (int)L;	
	long double ret = 0.0L;
	ret = sin(theLattice[nm][s2][s3] - angle) + sin(angle - theLattice[np][s2][s3]);
	return ret;
}
long double Lattice3DXY::sinY(int &s1, int &s2, int &s3,long double &angle){
	int np = (s2 + 1) %(int)L;
	int nm = (s2 -1 + (int)L) % (int)L;	
	long double ret = 0.0L;
	ret = sin(theLattice[s1][nm][s3] - angle) + sin(angle - theLattice[s1][np][s3]);
	return ret;
}
long double Lattice3DXY::sinZ(int &s1, int &s2, int &s3,long double &angle){
	int np = (s3 + 1) %(int)L;
	int nm = (s3 -1 + (int)L) % (int)L;	
	long double ret = 0.0L;
	ret = sin(theLattice[s1][s2][nm] - angle) + sin(angle - theLattice[s1][s2][np]);
	return ret;
}
;
long double calcSinX(long double ***lattice,long double  L){
	long double sum = 0.0L;
	for (int i =0; i< L; ++i){
		for (int j =0; j< L ; ++j){
			for (int k = 0; k<L; ++k){
				sum += sin(lattice[i][j][k] - lattice[(i+1)%(int)L][j][k]);
			}
		}
	}
	return sum;
}
long double calcSinY(long double ***lattice,long double  L){
	long double sum = 0.0L;
	for (int i =0; i< L; ++i){
		for (int j =0; j< L ; ++j){
			for (int k = 0; k<L; ++k){
				sum += sin(lattice[i][j][k] - lattice[i][(j+1)%(int)L][k]);
			}
		}
	}
	return sum;
}
long double calcSinZ(long double ***lattice,long double  L){
	long double sum = 0.0L;
	for (int i =0; i< L; ++i){
		for (int j =0; j< L ; ++j){
			for (int k = 0; k<L; ++k){
				sum += sin(lattice[i][j][k] - lattice[i][j][(k+1)%(int)L]);
			}
		}
	}
	return sum;
}

long double calcXMag(long double ***lattice,long double L){
	long double ret = 0.0L;
	for (int i = 0; i<L; ++i){
		for (int j = 0; j<L; ++j){
			for (int k = 0; k<L; ++k){
				ret += cos(lattice[i][j][k]);
			}
		}
	}
	return ret;
}
long double calcYMag(long double ***lattice,long double L){
	long double ret = 0.0L;
	for (int i = 0; i<L; ++i){
		for (int j = 0; j<L; ++j){
			for (int k = 0; k<L; ++k){
				ret += sin(lattice[i][j][k]);
			}
		}
	}
	return ret;
}

long double calcMag(long double ***lattice,long double L){
	long double mag = sqrt(pow(calcXMag(lattice,L),2) + pow(calcYMag(lattice,L),2));
	return mag;
}	

long double calcEn(Lattice3DXY* lat){
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
void Lattice3DXY::updateQuants(){
	energy = calcEn(this);
	xmag = calcXMag(theLattice,L);
	ymag = calcYMag(theLattice,L);
	sinx = calcSinX(theLattice,L);
	siny = calcSinY(theLattice,L);
	sinz = calcSinZ(theLattice,L);
};

//initialize new lattice
Lattice3DXY::Lattice3DXY(int l,long double rT, bool cold,RandStruct r,Cluster c) 
	:  rand(r),clust(c) 

{
	theLattice = newLattice((long double)l,cold);
	runTemp = rT;
	beta = 1.0L/rT;
	L = (long double)l;
	Nspins =L*L*L;
	Neqsweeps = 0.0L;
	NTotSweeps= 0.0L;
	Neqclusts = 0;
	NTotClusts= 0;
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
		energy = calcEn(this);
		xmag = calcXMag(theLattice,L);
		ymag = calcYMag(theLattice,L); 
		sinx = calcSinX(theLattice,L);
		siny = calcSinY(theLattice,L);
		sinz = calcSinZ(theLattice,L);
	}


};
Lattice3DXY::Lattice3DXY(){

}

void Lattice3DXY::testConsistent(){

	typedef std::numeric_limits<long double> dbl;
	std::cout.precision(dbl::max_digits10 + 5);
	long double testSinX = calcSinX(theLattice,L);
	long double testSinY = calcSinY(theLattice,L);
	long double testSinZ = calcSinZ(theLattice,L);
	long double testEn = calcEn(this);
	long double testXMag = calcXMag(theLattice,L);
	long double testYMag = calcYMag(theLattice,L);
	long double TotEn = energy;
	long double TotXMag= xmag;
	long double TotYMag= ymag;
	long double TotSinX= sinx;
	long double TotSinY = siny;
	long double TotSinZ = sinz;
	std::cout <<std::fixed<< TotEn - testEn << "  E    "<< TotEn << " "<< testEn << std::endl;
	std::cout <<std::fixed<< TotXMag - testXMag << "  X    "<< TotXMag << " "<< testXMag << std::endl;
	std::cout <<std::fixed<< TotYMag - testYMag << "  Y    "<< TotYMag << " "<< testYMag << std::endl;
	std::cout <<std::fixed<< TotSinX - testSinX << "  Sx    "<< TotSinX << " "<< testSinX << std::endl;
	std::cout <<std::fixed<< TotSinY - testSinY << "  Sy    "<< TotSinY << " "<< testSinY << std::endl;
	std::cout <<std::fixed<< TotSinZ - testSinZ << "  Sz    "<< TotSinZ << " "<< testSinZ << std::endl;
	//new test of magnetization
	long double sitemag;
	long double accum = 0.0L;
	for (int i = 0; i< L; ++i){
		for (int j = 0; j< L; ++j){
			for (int k = 0; k<L; ++k){	
				sitemag = std::pow(sin(theLattice[i][j][k]),2.0L) + 
					std::pow(cos(theLattice[i][j][k]),2.0L);
				std::cout << std::fixed << sitemag << std::endl;
				accum += std::abs(sitemag - 1.0L);
			}
		}
	}
	std::cout << std::fixed << accum << std::endl;
}
