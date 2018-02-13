
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

void wolffRun(long double L,long double ***lattice,long double Neq_sweeps,long double Neq_clusts, long double N_sample_sweeps,bool cold,long double Temperature){

	//initialize rng
	unsigned long int s;
	syscall(SYS_getrandom,&s,sizeof(unsigned long int),0);	
	std::uniform_real_distribution<long double> dist(0.0L,1.0L);
	std::mt19937_64 eng; 
	eng.seed(s);

	long double Beta = 1.0L/Temperature;		


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

	long double TotEn = calcEn(lattice,L);
	long double TotXMag = calcXMag(lattice,L);
	long double TotYMag = calcYMag(lattice,L);
	long double TotSinX = calcSinX(lattice,L);
	long double TotSinY = calcSinY(lattice,L);
	long double TotSinZ = calcSinZ(lattice,L);


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

	int steps = 0;
	int Nsample_clusts = 0;
	long double leaststeps = N_sample_sweeps*L*L*L;
	while (steps < leaststeps){
		//make a cluster
		steps += growCluster(lattice,cluster,L,Beta,TotXMag,TotYMag,TotEn,TotSinX,TotSinY,TotSinZ,dist,eng);
		++Nsample_clusts;

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
	long double actNsamp_sweeps = (long double)steps/(L*L*L);

	//define some reciprocals to reduce number of divions
	long double reciNsample_clusts= 1.0L/(long double)Nsample_clusts;
	long double reciNspins = 1.0L/(L*L*L);

	//calculate quantities of interest

	long double Eps = 0.0L;//energy per spin
	long double Mps = 0.0L;//magnetization per spin
	long double xi = 0.0L;//susceptibility
	long double b = 0.0L; //Binder parameter
	long double dbdt = 0.0L;//derivative wrt T of Binder parameter
	long double rs = 0.0L;//superfluid density


	//normalize
	avgE *= reciNsample_clusts;
	avgE2 *= reciNsample_clusts;
	avgM *= reciNsample_clusts;
	avgM2 *= reciNsample_clusts;
	avgM4 *= reciNsample_clusts;
	avgM2E *= reciNsample_clusts;
	avgM4E *= reciNsample_clusts;
	avgSinX2 *= reciNsample_clusts;
	avgSinY2 *= reciNsample_clusts;
	avgSinZ2 *= reciNsample_clusts;

	//calculate
	b = avgM4;
	b /= (avgM2*avgM2);
	dbdt = avgM4E*avgM2 + avgM4*avgM2*avgE - 2.0L*avgM4*avgM2E;
	dbdt *= Beta*Beta;
	dbdt /= avgM2*avgM2*avgM2;
	xi = avgM2 - avgM*avgM;
	xi *= reciNspins;
	xi *= Beta;
	rs = -avgE - (Beta)*avgSinX2 -(Beta)*avgSinY2 -(Beta)*avgSinZ2;
	rs *= (1.0L/3.0L)*L*reciNspins; 

	Eps = avgE*reciNspins;
	Mps = avgM*reciNspins;
	printOutput(L,Temperature,Eps,Mps,b,dbdt,xi,rs,Neq_sweeps,Neq_clusts,actNsamp_sweeps,Nsample_clusts,cold);

}
