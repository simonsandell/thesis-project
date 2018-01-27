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
	return ret;
}
// Method that performs one sweep on the lattice
void update(int **lattice, double L, double *probs, double &TotEnergy, double &TotMag,auto &randgen){
	int s1;
	int s2;
	int NN;
	int diffEn;
	double w;
	double p;
	//do one sweep
	for (int i = 0; i< L*L; ++i){
		s1 =  L*randgen();
		s2 =  L*randgen();
		NN = nnSum(lattice,L,s1,s2);
		//test of acceptance
		diffEn = 4*lattice[s1][s2]*NN;	
		if ( diffEn == 16) { w = probs[0];}
		else if ( diffEn == 8) { w = probs[1];}
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
	if (argc != 4 ){
		cout << "Usage: ./a.out <L> <N_equil> <startM>" << endl;
		return -1;
	}
	double L = stod(argv[1]);
	double equilibrationtime = stod(argv[2]);
	double startM = stod(argv[3]);
	double T = 2.26918531421;
	double beta = 1/T;

	//calculate energy differences beforehand
	double probs[2] = {exp(-16*beta),exp(-8*beta)};

	double TotEnergy;
	double TotMag;

	//define and initialize the lattice
	int **lattice;
	lattice = new int*[(int)L];
	for (int i = 0; i< L;++i){
		lattice[i] = new int[(int)L];
	}
	if ( startM == 1) {
		for (int i = 0; i<L;++i){
			for (int j=0; j<L;++j){
				lattice[i][j] = 1;
			}
		}
		TotEnergy =  -4*L*L;
		TotMag = L*L;
	}
	if ( startM == 0) {
		double k = 1;
		for ( int i = 0; i< L; ++i){
			for( int j = 0; j<L; ++j){
				k = -k;
				lattice[i][j] =k;
			}
		}
		TotMag = 0;
		TotEnergy = 0;

	}


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


	//test that energy and mag is correct after running
	/*
	   testEn = calcEn(lattice,L);
	   testMag = calcMag(lattice,L);
	   cout << testEn << " " << TotEnergy << endl;
	   cout << testMag<< " " << TotMag<< endl;
	   */
	//output to terminal

	cout << equilibrationtime << " " << abs(TotMag) << endl;

}
