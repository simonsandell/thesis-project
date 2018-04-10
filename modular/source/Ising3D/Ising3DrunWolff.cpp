
#include <iostream>
#include <random>
#include <functional>
#include <sys/syscall.h>
#include <unistd.h>
#include <linux/random.h>

#include "Ising3Dwolff.h"
#include "Ising3Dio.h"
#include "../clusterStruct.h"
#include "../randStruct.h"
#include "../avgStruct.h"
#include "../maxEHandle.h"

void wolffHistRunIsing3D(LatticeIsing3D& lat, long double N_sample_sweeps,long double *Temperatures,int N_temps){


	//convert temp to betas
	long double Betas[N_temps];	
	for (int i = 0; i< N_temps; ++i){
		Betas[i] = 1.0L/Temperatures[i];
	}


	//update lattice quantities
	lat.updateQuants();

	//make vector to hold separate averages for each temperature
	std::vector<avgStruct> avgs;
	for (int i = 0; i< N_temps; ++i){
		avgs.push_back(avgStruct());
	}

	long double expFac = 0.0L;
	long double maxTotE = lat.maxE; 
	//correction value for when current lattice energy becomes greater than saved maxE. If not zero by the end, write new value to files.
	long double expCorr = 0.0L;

	long double tE = 0.0L;
	long double tM = 0.0L;
	long double tM2 = 0.0L;

	long double steps = 0;//steps done in current cluster

	long double doneSweeps = 0.0L;//total done sweeps
	long double doneClusts = 0.0L;//total number of done clusters
	while (doneSweeps < N_sample_sweeps){
		//make a cluster
		steps = clusterIsing3D(lat);
		doneSweeps += steps/lat.Nspins;
		doneClusts += 1.0L;
		if (steps < 0.0L || doneSweeps < 0.0L) {
			std::cout << "OVERFLOW" << std::endl;
		}

		//update maxE if necessary
		
		if (abs(lat.energy)> abs(maxTotE)) {
			expCorr = 1.0L;
			if (doneClusts > 1.0L){
				expCorr = exp(-maxTotE +lat.energy);	
				for (int k = 0; k<N_temps;++k){
					avgs[k].e     *= expCorr;
					avgs[k].e2     *= expCorr;
					avgs[k].m     *= expCorr;
					avgs[k].m2     *= expCorr;
					avgs[k].m4     *= expCorr;
					avgs[k].m2e     *= expCorr;
					avgs[k].m4e     *= expCorr;
					avgs[k].exp     *= expCorr;
				}
			}
			maxTotE = lat.energy;
		}
		//take sample data
		tE = lat.energy/lat.Nspins;
		tM = std::abs(lat.mag/lat.Nspins);
		tM2 = lat.mag*lat.mag; 
		tM2 /= lat.Nspins*lat.Nspins;
		for (int i = 0; i<N_temps; ++i){
			expFac = exp(-(Betas[i] - lat.beta)*(lat.energy-maxTotE));
			avgs[i].exp += expFac;

			avgs[i].e += expFac*tE;
			avgs[i].e2+=expFac*tE*tE;
			avgs[i].m += expFac*tM;
			avgs[i].m2 += expFac*tM2;
			avgs[i].m4 += expFac*tM2*tM2;
			avgs[i].m2e += expFac*tM2*tE; 
			avgs[i].m4e += expFac*tM2*tM2*tE;
		}
	}//end of samples

	//calculate quantities of interest

	long double c[N_temps];//heat capacity
	long double xi[N_temps];//susceptibility
	long double b[N_temps]; //Binder parameter
	long double dbdt[N_temps];//derivative wrt T of Binder parameter
	for (int i =0; i< N_temps; ++i){


		//normalize
		avgs[i].e   /= doneClusts;
		avgs[i].e2  /= doneClusts;
		avgs[i].m   /= doneClusts;
		avgs[i].m2  /= doneClusts;
		avgs[i].m4  /= doneClusts;
		avgs[i].m2e /= doneClusts;
		avgs[i].m4e /= doneClusts;
		avgs[i].exp /= doneClusts;

		//calculate
		b[i] = avgs[i].m4*avgs[i].exp;
		b[i] /= (avgs[i].m2*avgs[i].m2);
		dbdt[i] = avgs[i].exp*avgs[i].m4e*avgs[i].m2 
			+ avgs[i].m4*avgs[i].m2*avgs[i].e 
			- 2.0L*avgs[i].exp*avgs[i].m4*avgs[i].m2e;
		dbdt[i] *= lat.Nspins;
		dbdt[i] /= Temperatures[i]*Temperatures[i]*avgs[i].m2*avgs[i].m2*avgs[i].m2;
		xi[i] = (avgs[i].m2/avgs[i].exp) -
				((avgs[i].m*avgs[i].m)/(avgs[i].exp*avgs[i].exp));
		xi[i] /= (Temperatures[i]);
		xi[i] *= lat.Nspins;

		c[i] = (avgs[i].e2/avgs[i].exp)	- (avgs[i].e*avgs[i].e/(avgs[i].exp*avgs[i].exp));
		c[i] /= Temperatures[i]*Temperatures[i];
		c[i] *= lat.Nspins*lat.Nspins;
	}
	for (int i = 0;i< N_temps; ++i){
		printIsing3DOutput(lat,Temperatures[i],avgs[i],
				b[i],dbdt[i],xi[i],c[i]);
	}
	if (expCorr != 0.0L){
		setMaxE(lat.maxEPath,lat.L,maxTotE);
	}
}
