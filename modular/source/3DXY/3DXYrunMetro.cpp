#include <iostream>
#include <random>
#include <functional>
#include <sys/syscall.h>
#include <unistd.h>
#include <linux/random.h>

#include "3DXYio.h"
#include "3DXYmetro.h"
#include "3DXYlattice.h"
#include "../randStruct.h"
#include "../avgStruct.h"


void metroRun3DXY(Lattice3DXY&lat, long double N_sample_sweeps,long double Temperature){

	//initialize rng
	RandStruct rand;

	long double Beta = 1.0L/Temperature;		

	lat.Nsmclusts = 0;
	lat.Nsmsweeps = N_sample_sweeps;

	lat.updateQuants();

	avgStruct avgs;
	avgs.exp = 1.0L;

	long double tE;
	long double tM2;
	long double tSx;
	long double tSy;
	long double tSz;
	for (int i = 0; i < N_sample_sweeps; ++i){
		//do 2 sweeps
		metrosweep3DXY(lat,Beta,rand);
		metrosweep3DXY(lat,Beta,rand);
		//scale quantities by lattice sites
		tE = lat.energy/lat.Nspins;
		tM2 = lat.xmag*lat.xmag + lat.ymag*lat.ymag;
		tM2 /= lat.Nspins*lat.Nspins;
		tSx = lat.sinx/lat.Nspins;
		tSy = lat.siny/lat.Nspins;
		tSz = lat.sinz/lat.Nspins;
		//take sample
		avgs.e += tE;
		avgs.e2+= tE*tE;
		avgs.m += sqrt(tM2);
		avgs.m2+= tM2;
		avgs.m4+= tM2*tM2; 
		avgs.m2e+= tM2*tE;
		avgs.m4e+= tM2*tM2*tE;
		avgs.s2x+= tSx*tSx;
		avgs.s2y+= tSy*tSy;
		avgs.s2z+= tSz*tSz;
	}

	//define _some reciprocals to reduce number of divions

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
	dbdt *= lat.Nspins;
	xi = avgs.m2 - avgs.m*avgs.m;
	xi /= Temperature;
	xi *= lat.Nspins;
	rs = -avgs.e 
		-lat.Nspins*(Beta)*avgs.s2x 
		-lat.Nspins*(Beta)*avgs.s2y
		-lat.Nspins*(Beta)*avgs.s2z;
	rs /= 3.0L; 
	rs *= lat.L;

	print3DXYOutput(lat,Temperature,avgs,b,dbdt,xi,rs);
}
