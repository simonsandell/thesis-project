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
#include "latticeStruct.h"
#include "randStruct.h"


void metroRun(Lattice&lat, long double N_sample_sweeps,long double Temperature){

	//initialize rng
	RandStruct rand;

	long double Beta = 1.0L/Temperature;		

	lat.Nsmclusts = 0;
	lat.Nsmsweeps = N_sample_sweeps;

	lat.updateQuants();



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
		metrosweep(lat,Beta,rand);
		metrosweep(lat,Beta,rand);
		//take sample data
		avgE += lat.energy;
		avgE2 += lat.energy*lat.energy;
		avgM += sqrt(lat.xmag*lat.xmag + lat.ymag*lat.ymag);
		avgM2 += (lat.xmag*lat.xmag + lat.ymag*lat.ymag);
		avgM4 += (lat.xmag*lat.xmag + lat.ymag*lat.ymag)*(lat.xmag*lat.xmag + lat.ymag*lat.ymag);
		avgM2E += lat.energy*(lat.xmag*lat.xmag + lat.ymag*lat.ymag); 
		avgM4E += lat.energy*(lat.xmag*lat.xmag + lat.ymag*lat.ymag)*(lat.xmag*lat.xmag + lat.ymag*lat.ymag);
		avgSinX2 += lat.sinx*lat.sinx;
		avgSinY2 += lat.siny*lat.siny;
		avgSinZ2 += lat.sinz*lat.sinz;
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
	xi /= Temperature*lat.Nspins;
	rs = -avgE - (Beta)*avgSinX2 -(Beta)*avgSinY2 -(Beta)*avgSinZ2;
	rs /= 3.0L*lat.L*lat.L; 

	printOutput(lat.L,Temperature,
			lat.Neqsweeps,lat.Neqclusts,
			lat.Nsmsweeps,lat.Nsmclusts,lat.coldstart,
			avgE,avgE2,avgM,avgM2,avgM4,
			avgM2E,avgM4E,
			avgSinX2,avgSinY2,avgSinZ2,
			b,dbdt,xi,rs,
			1.0L);
}
