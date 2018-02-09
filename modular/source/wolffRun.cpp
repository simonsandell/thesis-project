
#include <iostream>
#include <random>
#include <functional>
#include <sys/syscall.h>
#include <unistd.h>
#include <linux/random.h>

#include "wolff.h"
#include "calcQuants.h"
#include "latticeOps.h"
#include "ioFuncs.h"


void wolffRun(long double L, long double N_equil_sweeps, long double Nsamples,bool cold,long double Temperature){

	//initialize rng
	unsigned long int s;
	syscall(SYS_getrandom,&s,sizeof(unsigned long int),0);	
	std::uniform_real_distribution<long double> dist(0.0L,1.0L);
	std::mt19937_64 eng; 
	eng.seed(s);

	//convert temp to betas
	long double Beta = 1.0L/Temperature;		
	//define some reciprocals to reduce number of divions
	long double reciNsamples = 1.0L/Nsamples;
	long double reciNspins = 1.0L/(L*L*L);
	long double Nspins = (L*L*L);

	//initialize lattice
	long double *** lattice = newLattice(L,cold,dist,eng);

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

	long double TotEn = calcEn(lattice,L);
	long double TotXMag = calcXMag(lattice,L);
	long double TotYMag = calcYMag(lattice,L);
	long double TotSinX = calcSinX(lattice,L);
	long double TotSinY = calcSinY(lattice,L);
	long double TotSinZ = calcSinZ(lattice,L);

	//Set equilibration time 
	long double N_equil_steps= N_equil_sweeps*L*L*L;
	//eqilibration 
	int totEqSteps= 0;
	int eqClusts = 0;
	while (totEqSteps < N_equil_steps){
		eqClusts++;
		totEqSteps += growCluster(lattice,cluster,L,Beta,TotXMag,TotYMag,TotEn,TotSinX,TotSinY,TotSinZ,dist,eng);
	}
	long double eqSweeps = ((long double)totEqSteps)/Nspins;

	//start collecting data
	//parameters and physical quantities
	//averages
	long double avgE = 0.0L; //energy
	long double avgE2 = 0.0L;//squared energy
	long double avgM = 0.0L; //abs of magnetization
	long double avgM2 = 0.0L;//squared magnetization
	long double avgM4 = 0.0L;//fourth power of magnetization
	long double avgM2E = 0.0L;// squared magnetization times energy
	long double avgM4E = 0.0L; // 4th power magnetization times energy
	long double avgSinX2 = 0.0L; // for superfluid density 
	long double avgSinY2 = 0.0L; // for superfluid density 
	long double avgSinZ2 = 0.0L; // for superfluid density 



	for ( int i = 0; i < Nsamples; ++i){
		//make a cluster
		growCluster(lattice,cluster,L,Beta,TotXMag,TotYMag,TotEn,TotSinX,TotSinY,TotSinZ,dist,eng);
		//take sample data
		avgE += TotEn;
		avgE2 += TotEn*TotEn;
		avgM += sqrt(TotXMag*TotXMag + TotYMag*TotYMag);
		avgM2 += (TotXMag*TotXMag + TotYMag*TotYMag);
		avgM4 += (TotXMag*TotXMag + TotYMag*TotYMag)*(TotXMag*TotXMag + TotYMag*TotYMag);
		avgM2E += TotEn*(TotXMag*TotXMag + TotYMag*TotYMag); 
		avgM4E += TotEn*(TotXMag*TotXMag + TotYMag*TotYMag)*(TotXMag*TotXMag + TotYMag*TotYMag);
		avgSinX2 += TotSinX*TotSinX;
		avgSinY2 += TotSinY*TotSinY;
		avgSinZ2 += TotSinZ*TotSinZ;
	}


	//calculate quantities of interest

	//normalize
	avgE /= Nsamples;
	avgE2 /= Nsamples;
	avgM /= Nsamples;
	avgM2 /= Nsamples;
	avgM4 /= Nsamples;
	avgM2E /= Nsamples;
	avgM4E /= Nsamples;
	avgSinX2 /= Nsamples;
	avgSinY2 /= Nsamples;
	avgSinZ2 /= Nsamples;
	

	//derived quantites
	long double xi = 0.0L;//susceptibility
	long double b = 0.0L; //Binder parameter
	long double dbdt = 0.0L;//derivative wrt T of Binder parameter
	long double rs = 0.0L;//superfluid density
	long double Eps = avgE/Nspins;//energy per spin
	long double Mps = avgM/Nspins;//mag per spin
	//calculate
	
	b = avgM4/(avgM2*avgM2);
	dbdt = avgM4E*avgM2 + avgM4*avgM2*avgE - 2.0L*avgM4*avgM2E;
	dbdt /= avgM2*avgM2*avgM2;
	dbdt /= Temperature*Temperature;
	xi = avgM2 - avgM*avgM;
	xi /= (Nspins*Temperature);
	rs = (-(avgE/(L*L*3.0L))- (avgSinX2/(Temperature*L*L*3.0L)) - (avgSinY2/(Temperature*L*L*3.0L)) -(avgSinZ2/(Temperature*L*L*3.0L))) ;
	printOutput(L,Temperature,Eps,Mps,b,dbdt,xi,rs,eqSweeps,eqClusts,cold);
	
}
