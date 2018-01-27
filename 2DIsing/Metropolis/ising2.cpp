//This program performs the metropolis monecarlo simulation of the 2D Ising model
#include <iostream>
#include <cmath>
#include <random>
#include <functional>
#include <unistd.h>
#include <sys/syscall.h>
#include <linux/random.h>
#include <unistd.h>

using namespace std;

//calculate the sum of nearest neighbours
int nnSum(int **lattice,double &L,int& s1, int& s2){
	//find indices
	int p1 = (s1 + 1) % (int)L;
	int p2 = (s2 + 1) % (int)L;
	int m1 = (s1 - 1 + (int)L) % (int)L;
	int m2 = (s2 - 1 + (int)L) % (int)L;
	return lattice[p1][s2] + lattice[m1][s2] + lattice[s1][p2] + lattice[s1][m2];
}

//calc Energy by sweeping over lattice
double calcEn(int**lattice,double &L){
	double ret = 0;
	for ( int i = 0; i < L; ++i){
		for(int j=0;j< L; ++j){
			ret += -lattice[i][j]*nnSum(lattice,L,i,j);
		}
	}			
	//avoid double counting
	ret = 0.5*ret;
	return ret;
}	
//calc Magnetization by sweeping over lattice
double calcMag(int** lattice,double &L){
	double ret = 0;
	for ( int i = 0; i<L;++i){
		for(int j = 0; j< L; ++j){
			ret += lattice[i][j];
		}
	}
	ret = abs(ret);
	return ret;
}
// Method that performs one sweep on the lattice
void update(int **lattice, double L, double *probs, double &TotEnergy, double &TotMag,auto &randgen){
	int s1;
	int s2;
	double NN;
	double diffEn;
	double w;
	double p;
	//do one sweep
	for (int i = 0; i< L*L; ++i){
		s1 =  L*randgen();
		s2 =  L*randgen();
		NN = nnSum(lattice,L,s1,s2);
		diffEn = 2*lattice[s1][s2]*NN;	
		if ( diffEn == 8) { w = probs[0];}
		else if ( diffEn == 4) { w = probs[1];}
		else { w = 1;}
		p = randgen();
		if (p < w){
			lattice[s1][s2] = -lattice[s1][s2];
			TotEnergy += diffEn;
			TotMag += 2*lattice[s1][s2];
		}
	}
}

int main(int argc, char* argv[]){
	//generate random seed from system and initialize random number generator
	unsigned long int s;
	syscall(SYS_getrandom,&s,sizeof(unsigned long int),0);	
	uniform_real_distribution<double> dist(0,1);
	mt19937_64 eng; 
	eng.seed(s);
	auto gen = bind(dist,eng);

	//parameters and physical quantities
	//averages
	double avgE; //energy
	double avgE2;//squared energy
	double avgM; //abs of magnetization
	double avgM2;//squared magnetization
	double avgM4;//fourth power of magnetization
	double avgM2E;// squared magnetization times energy
	double avgM4E; // 4th power magnetization times energy

	//derived quantites
	double xi;//susceptibility
	double b; //binding param
	double dbdt;//derivative wrt T of binding param

	//set system size and temperature from input arguments
	if (argc != 3 ){
		cout << "Usage: ./a.out <L> <T>" << endl;
		return -1;
	}
	double L = stod(argv[1]);
	double T = stod(argv[2]);
	double beta = 1/T;

	//calculate energy differences beforehand
	double probs[2] = {exp(-8*beta),exp(-4*beta)};

	//define and initialize the lattice with all spins up
	int **lattice;
	lattice = new int*[(int)L];
	for (int i = 0; i< L;++i){
		lattice[i] = new int[(int)L];
	}
	for (int i = 0; i<L;++i){
		for (int j=0; j<L;++j){
			lattice[i][j] = 1;
		}
	}
	double TotEnergy =  -2*L*L;
	double TotMag = L*L;

	//equilibration takes 1000 sweeps
	double equilibrationtime = 10000;
	//take 10^5 samples
	double Nsamples = 100000; 
	

	//test that energy and mag is correct before running
	/*
	double testEn = calcEn(lattice,L);
	double testMag = calcMag(lattice,L);
	cout << testEn << " " << TotEnergy << endl;
	cout << testMag<< " " << TotMag<< endl;
	*/
	
	//eqilibration 
	for ( int i = 0; i < equilibrationtime; ++i){
		update(lattice, L, probs,TotEnergy,TotMag,gen);
	}

	//start collecting data
	avgE = 0;
	avgE2 = 0;
	avgM = 0;
	avgM2 = 0;
	avgM4 = 0;
	avgM2E = 0;
	avgM4E = 0;

	for ( int i = 0; i < Nsamples; ++i){
		//do 2 sweeps between each sample
		update(lattice,L,probs,TotEnergy,TotMag,gen);
		update(lattice,L,probs,TotEnergy,TotMag,gen);
		avgE += TotEnergy;
		avgE2 += TotEnergy*TotEnergy;
		avgM += abs(TotMag);
		avgM2 += TotMag*TotMag;
		avgM4 += TotMag*TotMag*TotMag*TotMag;
		avgM2E += TotMag*TotMag*TotEnergy;
		avgM4E += TotMag*TotMag*TotMag*TotMag*TotEnergy;
	}
	//test that energy and mag is correct after running
	/*
	double testEn = calcEn(lattice,L);
	double testMag = calcMag(lattice,L);
	cout << testEn << " " << TotEnergy << endl;
	cout << testMag<< " " << TotMag<< endl;
	*/

	//normalize
	avgE /= Nsamples;
	avgE2 /= Nsamples;
	avgM /= Nsamples;
	avgM2 /= Nsamples;
	avgM4 /= Nsamples;
	avgM2E /= Nsamples;
	avgM4E /= Nsamples;

	//calculate quantities of interest
	b = avgM4/(avgM2*avgM2);
	dbdt = (avgM4E/(avgM2*avgM2) + 2*avgM4*avgE/(avgM2*avgM2) - 3*avgM4*avgM2E/(avgM2*avgM2*avgM2));
	dbdt /= T*T;
	xi = avgM2 - avgM*avgM;
	xi /= L*L*T;

	//output to terminal
	cout << b << " " << dbdt << " " << xi;


}
