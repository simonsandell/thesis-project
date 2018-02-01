#include <iostream>
#include <cmath>
#include <random>
#include <functional>
#include <sys/syscall.h>
#include <unistd.h>
#include <linux/random.h>
#include <iomanip>
#include <utility>
#include <tuple>

#include "wolff.h"
#include "latticeOps.h"
#include "testFuncs.h"

using namespace std;

//main
int main(int argc, char* argv[]){

	//set precision of cout
	cout.precision(17);

	//generate random seed from system and initialize random number generator
	unsigned long int s;
	syscall(SYS_getrandom,&s,sizeof(unsigned long int),0);	
	uniform_real_distribution<double> dist(0.0,1.0);
	mt19937_64 eng; 
	eng.seed(s);

	//set system size and temperature from input arguments
	if (argc < 2){
		cout << "input arguments: L N_eq N_samp initM T_1 T_2 T_3 ..." << endl;
		exit(0);
	}
	double L = stod(argv[1]);
	double N_equil_sweeps = stod(argv[2]);
	double Nsamples = stod(argv[3]);
	double initM = stod(argv[4]);
	double N_temps = 1;
	double extT[argc - 5] = {};
	double extBeta[argc - 5] = {};
	N_temps = argc - 5;
	for (int i = 0; i< N_temps; ++i){
		extT[i] = stod(argv[i+5]);
		extBeta[i] = 1.0/extT[i];
	}
	double T = extT[(int)(N_temps/2)];
	double beta = 1.0/T;		


	double TotEn;
	double TotXMag;
	double TotYMag;
	double TotSinX;

	//
	//Set equilibration time and number of samples
	double N_equil_steps= N_equil_sweeps*L*L*L;

	//define and initialize the lattice and cluster
	double ***lattice;
	bool***cluster;
	lattice = new double **[(int)L];
	cluster = new bool**[(int)L];
	for (int i = 0; i< L;++i){
		lattice[i] = new double *[(int)L];
		cluster[i] = new bool*[(int)L];
		for (int j =0;j<L;++j){
			lattice[i][j] = new double[(int)L];
			cluster[i][j] = new bool[(int)L];
		}
	}

	if (initM == 0) {
		for (int i = 0; i<L;++i){
			for (int j=0; j<L;++j){
				for (int k = 0; k<L; ++k){
					lattice[i][j][k] = dist(eng)*2.0*M_PI;
					cluster[i][j][k] = 0;
				}
			}
		}
	TotEn = calcEn(lattice,L); 
	TotXMag = calcXMag(lattice,L); 
	TotYMag = calcYMag(lattice,L); 
	TotSinX = calcSinX(lattice,L); 
	}
	else {
		for (int i = 0; i<L;++i){
			for (int j=0; j<L;++j){
				for (int k = 0; k<L; ++k){
					lattice[i][j][k] = 0.5*M_PI;
					cluster[i][j][k] = 0;
				}
			}
		}
	TotEn = -3.0*L*L*L;
	TotXMag = 0.0;
	TotYMag = L*L*L; 
	TotSinX = 0.0;
	}

	//eqilibration 
	int t = 0;
	while (t < N_equil_steps){
		t += growCluster(lattice,cluster,L,beta,TotXMag,TotYMag,TotEn,TotSinX,dist,eng);
	}
	//start collecting data
	//parameters and physical quantities
	//averages
	double avgE[(int)N_temps] = {}; //energy
	double avgE2[(int)N_temps] = {};//squared energy
	double avgM[(int)N_temps] = {}; //abs of magnetization
	double avgM2[(int)N_temps] = {};//squared magnetization
	double avgM4[(int)N_temps] = {};//fourth power of magnetization
	double avgM2E[(int)N_temps] = {};// squared magnetization times energy
	double avgM4E[(int)N_temps] = {}; // 4th power magnetization times energy
	double avgSinX2[(int)N_temps] = {}; // for superfluid density 


	double avgExpFac[(int)N_temps] = {};
	double expFac;

	for ( int i = 0; i < Nsamples; ++i){
		//make a cluster
		growCluster(lattice,cluster,L,beta,TotXMag,TotYMag,TotEn,TotSinX,dist,eng);
		//take sample data
		for (int i = 0; i<N_temps; ++i){
			expFac = exp(-( ((extBeta[i])) - beta)*TotEn);
			avgExpFac[i] += expFac;
			avgE[i] += expFac*TotEn;
			avgE2[i] += expFac*TotEn*TotEn;
			avgM[i] += expFac*sqrt(TotXMag*TotXMag + TotYMag*TotYMag);

			avgM2[i] += expFac*(TotXMag*TotXMag + TotYMag*TotYMag);
			avgM4[i] += expFac*(TotXMag*TotXMag + TotYMag*TotYMag)*(TotXMag*TotXMag + TotYMag*TotYMag);
			avgM2E[i] += TotEn*expFac*(TotXMag*TotXMag + TotYMag*TotYMag); 
			avgM4E[i] += TotEn*expFac*(TotXMag*TotXMag + TotYMag*TotYMag)*(TotXMag*TotXMag + TotYMag*TotYMag);

			avgSinX2[i] += TotSinX*TotSinX*expFac;
		}

	}


	//calculate quantities of interest
	//define some reciprocals to reduce number of divions
	double reciNsamples = 1.0/Nsamples;
	double reciNspins = 1.0/(L*L*L);
	double reciExpFac = 0.0;
	//derived quantites
	double xi[(int)N_temps] = {};//susceptibility
	double b[(int)N_temps] = {}; //Binder parameter
	double dbdt[(int)N_temps] = {};//derivative wrt T of Binder parameter

	double rs[(int)N_temps] = {};//superfluid density
	for (int i =0; i< N_temps; ++i){

		//normalize
		avgExpFac[i] *= reciNsamples;
		reciExpFac = 1.0/avgExpFac[i];
		avgE[i] *= reciNsamples;
		avgE2[i] *= reciNsamples;
		avgM[i] *= reciNsamples;
		avgM2[i] *= reciNsamples;
		avgM4[i] *= reciNsamples;
		avgM2E[i] *= reciNsamples;
		avgM4E[i] *= reciNsamples;
		avgSinX2[i] *= reciNsamples;

		avgE[i] *= reciExpFac;
		avgE2[i] *= reciExpFac;
		avgM[i] *= reciExpFac;
		avgM2[i] *= reciExpFac;
		avgM4[i] *= reciExpFac;
		avgM2E[i] *= reciExpFac;
		avgM4E[i] *= reciExpFac;
		avgSinX2[i] *= reciExpFac;
		//calculate
		b[i] = avgM4[i];
		b[i] /= (avgM2[i]*avgM2[i]);
		dbdt[i] = avgM4E[i]*avgM2[i] + avgM4[i]*avgM2[i]*avgE[i] - 2.0*avgM4[i]*avgM2E[i];
		dbdt[i] *= extBeta[i]*extBeta[i];
		dbdt[i] /= avgM2[i]*avgM2[i]*avgM2[i];
		xi[i] = avgM2[i] - avgM[i]*avgM[i];
		xi[i] *= reciNspins;
		xi[i] *= extBeta[i];
		rs[i] = -(1.0/3.0)*avgE[i] - (1.0/extT[i])*avgSinX2[i];
		rs[i] *= L*reciNspins; 
	}
	for (int i = 0;i< N_temps; ++i){
		cout << fixed << L << " ";
		cout << fixed << extT[i] << " ";
		cout << fixed << avgE[i]*reciNspins << " ";
		cout << fixed << avgM[i]*reciNspins << " ";
		cout << fixed << b[i] << " ";
		cout << fixed << dbdt[i] << " ";
		cout << fixed << xi[i] << " ";
		cout << fixed << N_equil_sweeps << " "; 
		cout << fixed << rs[i] << " ";
		cout << fixed << endl;
	}
}
