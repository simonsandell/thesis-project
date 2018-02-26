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
#include "avgStruct.h"


void metroRun(Lattice&lat, long double N_sample_sweeps,long double Temperature){

	//initialize rng
	RandStruct rand;

	long double Beta = 1.0L/Temperature;		

	lat.Nsmclusts = 0;
	lat.Nsmsweeps = N_sample_sweeps;

	lat.updateQuants();

	avgStruct avgs;
	avgs.exp = 1.0L;













	for (int i = 0; i < N_sample_sweeps; ++i){
		metrosweep(lat,Beta,rand);
		metrosweep(lat,Beta,rand);
		//take sample data
		avgs.e += lat.energy;
		avgs.e2+= lat.energy*lat.energy;
		avgs.m += sqrt(lat.xmag*lat.xmag + lat.ymag*lat.ymag);
		avgs.m2+= (lat.xmag*lat.xmag + lat.ymag*lat.ymag);
		avgs.m4+= (lat.xmag*lat.xmag + lat.ymag*lat.ymag)*(lat.xmag*lat.xmag + lat.ymag*lat.ymag);
		avgs.m2e+= lat.energy*(lat.xmag*lat.xmag + lat.ymag*lat.ymag); 
		avgs.m4e+= lat.energy*(lat.xmag*lat.xmag + lat.ymag*lat.ymag)*(lat.xmag*lat.xmag + lat.ymag*lat.ymag);
		avgs.s2x+= lat.sinx*lat.sinx;
		avgs.s2y+= lat.siny*lat.siny;
		avgs.s2z+= lat.sinz*lat.sinz;
	}

	//define some reciprocals to reduce number of divions

	//calculate quantities of interest

	long double xi = 0.0L;//susceptibility
	long double b = 0.0L; //Binder parameter
	long double dbdt = 0.0L;//derivative wrt T of Binder parameter
	long double rs = 0.0L;//superfluid density


	//normalize
	avgs.e /= N_sample_sweeps;
	avgs.e2 /= N_sample_sweeps;
	avgs.m  /= N_sample_sweeps;
	avgs.m2 /= N_sample_sweeps;
	avgs.m4 /= N_sample_sweeps;
	avgs.m2e/= N_sample_sweeps;
	avgs.m4e/= N_sample_sweeps;
	avgs.s2x/= N_sample_sweeps;
	avgs.s2y/= N_sample_sweeps;
	avgs.s2z/= N_sample_sweeps;
	//calculate
	b = avgs.m4;
	b /= (avgs.m2*avgs.m2);
	dbdt = avgs.m4e*avgs.m2 + avgs.m4*avgs.m2*avgs.e - 2.0L*avgs.m4*avgs.m2e;
	dbdt /= Temperature*Temperature*avgs.m2*avgs.m2*avgs.m2;
	xi = avgs.m2 - avgs.m*avgs.m;
	xi /= Temperature*lat.Nspins;
	rs = -avgs.e - (Beta)*avgs.s2x -(Beta)*avgs.s2y-(Beta)*avgs.s2z;
	rs /= 3.0L*lat.L*lat.L; 

	printOutput(lat,Temperature,avgs,b,dbdt,xi,rs);
}
