
#include <iostream>
#include <random>
#include <functional>
#include <sys/syscall.h>
#include <unistd.h>
#include <linux/random.h>

#include "wolff.h"
#include "testFuncs.h"
#include "latticeOps.h"

void wolffRun(double L, double N_equil_sweeps, double N_samples,bool cold,double Temperature){

	//initialize rng
	unsigned long int s;
	syscall(SYS_getrandom,&s,sizeof(unsigned long int),0);	
	std::uniform_real_distribution<double> dist(0.0,1.0);
	std::mt19937_64 eng; 
	eng.seed(s);

	//convert temp to betas
	double Beta = 1.0/Temperature;		
	//define some reciprocals to reduce number of divions
	double reciNsamples = 1.0/N_samples;
	double reciNspins = 1.0/(L*L*L);

	//initialize lattice
	double *** lattice = newLattice(L,cold,dist,eng);

	//define and initialize cluster
	bool***cluster;
	cluster = new bool**[(int)L];
	for (int i = 0; i< L;++i){
		cluster[i] = new bool*[(int)L];
		for (int j =0;j<L;++j){
			cluster[i][j] = new bool[(int)L];
		}
	}
	for (int i = 0; i<L;++i){
		for (int j=0; j<L;++j){
			for (int k = 0; k<L; ++k){
				cluster[i][j][k] = false;
			}
		}
	}

	double TotEn = calcEn(lattice,L);
	double TotXMag = calcXMag(lattice,L);
	double TotYMag = calcYMag(lattice,L);
	double TotSinX = calcSinX(lattice,L);

	//Set equilibration time 
	double N_equil_steps= N_equil_sweeps*L*L*L;
	//eqilibration 
	int totEqSteps= 0;
	while (totEqSteps < N_equil_steps){
		totEqSteps += growCluster(lattice,cluster,L,Beta,TotXMag,TotYMag,TotEn,TotSinX,dist,eng);
	}
	double eqSweeps = double(totEqSteps)*reciNspins;

	//start collecting data
	//parameters and physical quantities
	//averages
	double avgE = 0.0; //energy
	double avgE2 = 0.0;//squared energy
	double avgM = 0.0; //abs of magnetization
	double avgM2 = 0.0;//squared magnetization
	double avgM4 = 0.0;//fourth power of magnetization
	double avgM2E = 0.0;// squared magnetization times energy
	double avgM4E = 0.0; // 4th power magnetization times energy
	double avgSinX2 = 0.0; // for superfluid density 



	for ( int i = 0; i < N_samples; ++i){
		//make a cluster
		growCluster(lattice,cluster,L,Beta,TotXMag,TotYMag,TotEn,TotSinX,dist,eng);
		//take sample data
		avgE += TotEn;
		avgE2 += TotEn*TotEn;
		avgM += sqrt(TotXMag*TotXMag + TotYMag*TotYMag);
		avgM2 += (TotXMag*TotXMag + TotYMag*TotYMag);
		avgM4 += (TotXMag*TotXMag + TotYMag*TotYMag)*(TotXMag*TotXMag + TotYMag*TotYMag);
		avgM2E += TotEn*(TotXMag*TotXMag + TotYMag*TotYMag); 
		avgM4E += TotEn*(TotXMag*TotXMag + TotYMag*TotYMag)*(TotXMag*TotXMag + TotYMag*TotYMag);
		avgSinX2 += TotSinX*TotSinX;
	}


	//calculate quantities of interest

	//normalize
	avgE *= reciNsamples;
	avgE2 *= reciNsamples;
	avgM *= reciNsamples;
	avgM2 *= reciNsamples;
	avgM4 *= reciNsamples;
	avgM2E *= reciNsamples;
	avgM4E *= reciNsamples;
	avgSinX2 *= reciNsamples;

	//derived quantites
	double xi = 0.0;//susceptibility
	double b = 0.0; //Binder parameter
	double dbdt = 0.0;//derivative wrt T of Binder parameter
	double rs = 0.0;//superfluid density
	//calculate
	b = avgM4;
	b /= (avgM2*avgM2);
	dbdt = avgM4E*avgM2 + avgM4*avgM2*avgE - 2.0*avgM4*avgM2E;
	dbdt *= Beta*Beta;
	dbdt /= avgM2*avgM2*avgM2;
	xi = avgM2 - avgM*avgM;
	xi *= reciNspins;
	xi *= Beta;
	rs = -(1.0/3.0)*avgE - Beta*avgSinX2;
	rs *= L*reciNspins; 
	std::cout << std::fixed << L << " ";
	std::cout << std::fixed << Temperature << " ";
	std::cout << std::fixed << avgE*reciNspins << " ";
	std::cout << std::fixed << avgM*reciNspins << " ";
	std::cout << std::fixed << b << " ";
	std::cout << std::fixed << dbdt << " ";
	std::cout << std::fixed << xi << " ";
	std::cout << std::fixed << eqSweeps << " "; 
	std::cout << std::fixed << rs << " ";
	std::cout << std::fixed << std::endl;
}
