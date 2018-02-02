
#include <iostream>
#include <random>
#include <functional>
#include <sys/syscall.h>
#include <unistd.h>
#include <linux/random.h>

#include "wolff.h"
#include "testFuncs.h"
#include "latticeOps.h"

void wolffHistRun(double L, double N_equil_sweeps, double N_samples,bool cold,double *Temperatures,int N_temps){

	//initialize rng
	unsigned long int s;
	syscall(SYS_getrandom,&s,sizeof(unsigned long int),0);	
	std::uniform_real_distribution<double> dist(0.0,1.0);
	std::mt19937_64 eng; 
	eng.seed(s);

	//convert temp to betas
	double Betas[N_temps];	
	for (int i = 0; i< N_temps; ++i){
		Betas[i] = 1.0/Temperatures[i];
	}
	double Temperature = Temperatures[(int)(N_temps/2)];
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
				cluster[i][j][k] = 0;
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

	double avgE[N_temps] = {}; //energy
	double avgE2[N_temps] = {};//squared energy
	double avgM[N_temps] = {}; //abs of magnetization
	double avgM2[N_temps] = {};//squared magnetization
	double avgM4[N_temps] = {};//fourth power of magnetization
	double avgM2E[N_temps] = {};// squared magnetization times energy
	double avgM4E[N_temps] = {}; // 4th power magnetization times energy

	double avgSinX2[N_temps] = {}; // for superfluid density 


	double avgExpFac[N_temps] = {};
	double expFac;

	for ( int i = 0; i < N_samples; ++i){
		//make a cluster
		growCluster(lattice,cluster,L,Beta,TotXMag,TotYMag,TotEn,TotSinX,dist,eng);
		//take sample data
		for (int i = 0; i<N_temps; ++i){
			expFac = exp(-(Betas[i] - Beta)*TotEn);
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
	double reciExpFac = 0.0;

	double xi[N_temps] = {};//susceptibility
	double b[N_temps] = {}; //Binder parameter
	double dbdt[N_temps] = {};//derivative wrt T of Binder parameter
	double rs[N_temps] = {};//superfluid density
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
		dbdt[i] *= Betas[i]*Betas[i];
		dbdt[i] /= avgM2[i]*avgM2[i]*avgM2[i];
		xi[i] = avgM2[i] - avgM[i]*avgM[i];
		xi[i] *= reciNspins;
		xi[i] *= Betas[i];
		rs[i] = -(1.0/3.0)*avgE[i] - (Betas[i])*avgSinX2[i];
		rs[i] *= L*reciNspins; 
	}
	for (int i = 0;i< N_temps; ++i){
		std::cout << std::fixed << L << " ";
		std::cout << std::fixed << Temperatures[i] << " ";
		std::cout << std::fixed << avgE[i]*reciNspins << " ";
		std::cout << std::fixed << avgM[i]*reciNspins << " ";
		std::cout << std::fixed << b[i] << " ";
		std::cout << std::fixed << dbdt[i] << " ";
		std::cout << std::fixed << xi[i] << " ";
		std::cout << std::fixed << N_equil_sweeps << " "; 
		std::cout << std::fixed << rs[i] << " ";
		std::cout << std::fixed << std::endl;

	}
}
