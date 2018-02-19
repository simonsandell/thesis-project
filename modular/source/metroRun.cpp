
#include <iostream>
#include <random>
#include <functional>
#include <sys/syscall.h>
#include <unistd.h>
#include <linux/random.h>

#include "calcQuants.h"
#include "latticeOps.h"
#include "ioFuncs.h"
#include "metropolis.h"

void metroRun(long double L,long double ***lattice,long double Neq_sweeps, long double N_sample_sweeps,bool cold,long double Temperature){

	//initialize rng
	unsigned long int s;
	syscall(SYS_getrandom,&s,sizeof(unsigned long int),0);	
	std::uniform_real_distribution<long double> dist(0.0L,1.0L);
	std::mt19937_64 eng; 
	eng.seed(s);

	long double Beta = 1.0L/Temperature;		


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

	for (int i = 0; i < N_sample_sweeps; ++i){
		metrosweep(lattice,L,Beta,TotXMag,TotYMag,TotEn,TotSinX,TotSinY,TotSinZ,dist,eng);
		metrosweep(lattice,L,Beta,TotXMag,TotYMag,TotEn,TotSinX,TotSinY,TotSinZ,dist,eng);
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

	//define some reciprocals to reduce number of divions

	//calculate quantities of interest

	long double xi = 0.0L;//susceptibility
	long double b = 0.0L; //Binder parameter
	long double dbdt = 0.0L;//derivative wrt T of Binder parameter
	long double rs = 0.0L;//superfluid density


	//normalize
	avgE /= N_sample_sweeps;
	avgE2 /= N_sample_sweeps;
	avgM /= N_sample_sweeps;
	avgM2 /= N_sample_sweeps;
	avgM4 /= N_sample_sweeps;
	avgM2E /= N_sample_sweeps;
	avgM4E /= N_sample_sweeps;
	avgSinX2 /= N_sample_sweeps;
	avgSinY2 /= N_sample_sweeps;
	avgSinZ2 /= N_sample_sweeps;

	//calculate
	b = avgM4;
	b /= (avgM2*avgM2);
	dbdt = avgM4E*avgM2 + avgM4*avgM2*avgE - 2.0L*avgM4*avgM2E;
	dbdt /= Temperature*Temperature*avgM2*avgM2*avgM2;
	xi = avgM2 - avgM*avgM;
	xi /= Temperature*L*L*L;
	rs = -avgE - (Beta)*avgSinX2 -(Beta)*avgSinY2 -(Beta)*avgSinZ2;
	rs /= 3.0L*L*L; 
		
	printOutput(L,Temperature,
				Neq_sweeps,0,
				N_sample_sweeps,0,cold,
				avgE,avgE2,avgM,avgM2,avgM4,
				avgM2E,avgM4E,
				avgSinX2,avgSinY2,avgSinZ2,
				b,dbdt,xi,rs,
				1.0L);
}
