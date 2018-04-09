#include <iostream>
#include <random>
#include <functional>
#include <sys/syscall.h>
#include <unistd.h>
#include <linux/random.h>

#include "3DXYwolff.h"
#include "3DXYio.h"
#include "../clusterStruct.h"
#include "../randStruct.h"
#include "../avgStruct.h"
#include "../maxEHandle.h"

void wolffHistRun3DXY(Lattice3DXY& lat, long double N_sample_sweeps,long double *Temperatures,int N_temps,long double runTemp){


	//convert temp to betas
	long double Betas[N_temps];	
	for (int i = 0; i< N_temps; ++i){
		Betas[i] = 1.0L/Temperatures[i];
		std::cout << Betas[i] << std::endl;
	}
	long double Beta = 1.0L/runTemp;		


	//update lattice quantities
	lat.updateQuants();

	//make vector to hold separate averages for each temperature
	std::vector<avgStruct> avgs;
	for (int i = 0; i< N_temps; ++i){
		avgs.push_back(avgStruct());
	}

	long double expFac = 0.0L;
	long double maxTotE = lat.maxE;
	long double expCorr = 0.0L;
	long double tE = 0.0L;
	long double tM2 = 0.0L;
	long double tSx = 0.0L;
	long double tSy = 0.0L;
	long double tSz = 0.0L;

	long double steps = 0.0L;
	long double doneSweeps = 0.0L;
	long double doneClusts = 0.0L;

	while (doneSweeps < N_sample_sweeps){
		//perform a cluster update
		steps = cluster3DXY(lat);
		doneSweeps += steps/lat.Nspins;
		doneClusts += 1.0L;
		if (doneSweeps< 0.0L || steps < 0.0L) {
			std::cout << "OVERFLOW" << std::endl;
		}

		//update maxE if necessary
		
		if (std::abs(lat.energy) > std::abs(maxTotE)){
			expCorr = 1.0L;
			if (doneClusts> 1.0L){
				expCorr = exp(-maxTotE +lat.energy);	
				for (int k = 0; k<N_temps;++k){
					avgs[k].e	*= expCorr;
					avgs[k].e2 	*= expCorr;
					avgs[k].m 	*= expCorr;
					avgs[k].m2	*= expCorr;
					avgs[k].m4 	*= expCorr;
					avgs[k].m2e     *= expCorr;
					avgs[k].m4e     *= expCorr;
					avgs[k].s2x     *= expCorr;
					avgs[k].s2y     *= expCorr;
					avgs[k].s2z     *= expCorr;
					avgs[k].exp     *= expCorr;
				}
			}
			maxTotE = lat.energy;
			lat.maxE = lat.energy;
		}
		//take sample data
		tE = lat.energy/lat.Nspins;
		tM2 = lat.xmag*lat.xmag + lat.ymag*lat.ymag;
		tM2 /= lat.Nspins*lat.Nspins;
		tSx = lat.sinx/lat.Nspins;
		tSy = lat.siny/lat.Nspins;
		tSz = lat.sinz/lat.Nspins;

		for (int i = 0; i<N_temps; ++i){
			expFac = exp(-(Betas[i] - Beta)*(lat.energy-maxTotE));
			avgs[i].exp += expFac;


			avgs[i].e += 	expFac*tE;
			avgs[i].e2+=	expFac*tE*tE;
			avgs[i].m += 	expFac*sqrt(tM2);
			avgs[i].m2 += 	expFac*tM2;
			avgs[i].m4 += 	expFac*tM2*tM2;
			avgs[i].m2e += 	expFac*tM2*tE; 
			avgs[i].m4e += 	expFac*tM2*tM2*tE;
			avgs[i].s2x += 	expFac*tSx*tSx;
			avgs[i].s2y += 	expFac*tSy*tSy;
			avgs[i].s2z += 	expFac*tSz*tSz;
		}
	}//end of samples




	//calculate quantities of interest

	long double xi[N_temps];//susceptibility
	long double b[N_temps]; //Binder parameter
	long double dbdt[N_temps];//derivative wrt T of Binder parameter
	long double rs[N_temps];//superfluid density
	for (int i =0; i< N_temps; ++i){

		//normalize
		avgs[i].e   /= doneClusts;
		avgs[i].e2  /= doneClusts;
		avgs[i].m   /= doneClusts;
		avgs[i].m2  /= doneClusts;
		avgs[i].m4  /= doneClusts;
		avgs[i].m2e /= doneClusts;
		avgs[i].m4e /= doneClusts;
		avgs[i].s2x /= doneClusts;
		avgs[i].s2y /= doneClusts;
		avgs[i].s2z /= doneClusts;
		avgs[i].exp /= doneClusts;

		//calculate
		b[i] = avgs[i].m4*avgs[i].exp;
		b[i] /= (avgs[i].m2*avgs[i].m2);
		dbdt[i] = avgs[i].exp*avgs[i].m4e*avgs[i].m2 
			+ avgs[i].m4*avgs[i].m2*avgs[i].e 
			- 2.0L*avgs[i].exp*avgs[i].m4*avgs[i].m2e;
		dbdt[i] *= lat.Nspins;
		dbdt[i] /= Temperatures[i]*Temperatures[i]*avgs[i].m2*avgs[i].m2*avgs[i].m2;
		xi[i] = ((avgs[i].m2/avgs[i].exp) -
				(avgs[i].m*avgs[i].m/(avgs[i].exp*avgs[i].exp)))*lat.Nspins;
		xi[i] /= (Temperatures[i]);
		rs[i] = -avgs[i].e 
			-lat.Nspins*avgs[i].s2x/Temperatures[i] 
			-lat.Nspins*avgs[i].s2y/Temperatures[i] 
			-lat.Nspins*avgs[i].s2z/Temperatures[i];
		rs[i] *= lat.L;
		rs[i] /= (3.0L*avgs[i].exp);
	}

	for (int i = 0;i< N_temps; ++i){
		print3DXYOutput(lat,Temperatures[i],avgs[i],
				b[i],dbdt[i],xi[i],rs[i]);
	}
	if (expCorr != 0.0L){
		setMaxE(lat.maxEPath,lat.L,maxTotE);
	}
}
