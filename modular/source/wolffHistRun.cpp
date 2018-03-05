
#include <iostream>
#include <random>
#include <functional>
#include <sys/syscall.h>
#include <unistd.h>
#include <linux/random.h>

#include "wolff.h"
#include "ioFuncs.h"
#include "clusterStruct.h"
#include "randStruct.h"
#include "avgStruct.h"

void wolffHistRun(Lattice& lat, long double N_sample_sweeps,long double *Temperatures,int N_temps,long double runTemp){


	//convert temp to betas
	long double Betas[N_temps];	
	for (int i = 0; i< N_temps; ++i){
		Betas[i] = 1.0L/Temperatures[i];
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
	long double maxTotE = getMaxE(lat.L); 
	long double expCorr = 0.0L;

	int steps = 0;
	int intNsampClust = 0;
	long double leaststeps = N_sample_sweeps*lat.Nspins;

	Cluster cluster(lat.L);
	RandStruct rand;

	while (steps < leaststeps){
		//make a cluster
		steps += growCluster(lat,cluster,Beta,rand);
		if (steps < 0) {
			std::cout << "OVERFLOW" << std::endl;
			exit(0);
		}
		++intNsampClust;

		//update maxE if necessary
		
		if ((maxTotE - lat.energy) > 0){
			expCorr = 1.0L;
			if (intNsampClust > 1){
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
		long double tE;
		long double tM;
		long double tM2;
		for (int i = 0; i<N_temps; ++i){
			expFac = exp(-(Betas[i] - Beta)*(lat.energy-maxTotE));
			avgs[i].exp += expFac;

			tE = lat.energy/lat.Nspins;
			tM = std::abs(lat.mag/lat.Nspins);
			tM2 = lat.mag*lat.mag + lat.mag*lat.mag;
			tM2 /= lat.Nspins*lat.Nspins;

			avgs[i].e += expFac*tE;
			avgs[i].e2+=expFac*tE*tE;
			avgs[i].m += expFac*tM;
			avgs[i].m2 += expFac*tM2;
			avgs[i].m4 += expFac*tM2*tM2;
			avgs[i].m2e += expFac*tM2*tE; 
			avgs[i].m4e += expFac*tM2*tM2*tE;
		}
	}//end of samples
	lat.Nsmclusts=long double(intNsampClust);
	lat.Nsmsweeps = ((long double)steps)/((long double)lat.Nspins);

	//calculate quantities of interest

	long double c[N_temps];//heat capacity
	long double xi[N_temps];//susceptibility
	long double b[N_temps]; //Binder parameter
	long double dbdt[N_temps];//derivative wrt T of Binder parameter
	for (int i =0; i< N_temps; ++i){

		//print values
		/*
		   std::cout <<"avgExpFac[i]"<<	       avgs[i].exp <<std::endl;
		   std::cout <<"avgE[i]     "<<        avgs[i].e <<std::endl;
		   std::cout <<"avgE2[i]     "<<        avgs[i].e2 <<std::endl;
		   std::cout <<"avgM[i]    "<<        avgs[i].m  <<std::endl;
		   std::cout <<"avgM2[i]     "<<        avgs[i].m2 <<std::endl;
		   std::cout <<"avgM4[i]    "<<        avgs[i].m4 <<std::endl;
		   std::cout <<"avgM2E[i]    "<<        avgs[i].m2e <<std::endl;
		   std::cout <<"avgM4E[i]   "<<        avgs[i].m4e<<std::endl;
		   */

		//normalize
		avgs[i].e   /= lat.Nsmclusts;
		avgs[i].e2  /= lat.Nsmclusts;
		avgs[i].m   /= lat.Nsmclusts;
		avgs[i].m2  /= lat.Nsmclusts;
		avgs[i].m4  /= lat.Nsmclusts;
		avgs[i].m2e /= lat.Nsmclusts;
		avgs[i].m4e /= lat.Nsmclusts;
		avgs[i].exp /= lat.Nsmclusts;

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

		c[i] = (avgs[i].e2/avgs[i].exp)	- (avgs[i].e*avgs[i].e/(avgs[i].exp*avgs[i].exp));
		c[i] /= Temperatures[i]*Temperatures[i];
		c[i] *= lat.Nspins*lat.Nspins;
		//print values
		/*
		   std::cout << "b = " << avgs[i].m4 << " * " << avgs[i].exp << std::endl;
		   std::cout << "b /= " << avgs[i].m2 << " * " << avgs[i].m2 << std::endl;
		   std::cout << "dbdt[i] = " << avgs[i].exp << " * " << avgs[i].m4e << 
		   " * " << avgs[i].m2<<" + "<< avgs[i].m4<< " * " <<avgs[i].m2<< 
		   " * " << avgs[i].e << " - 2.0L* " << avgs[i].exp<< " * " <<
		   avgs[i].m4 << " * " << avgs[i].m2e << std::endl;
		   std::cout << "dbdt[i] /= " << Temperatures[i] << "^2 * " << avgs[i].m2<< "^3" << std::endl;
		   std::cout << "xi[i] = " << " ( " << avgs[i].m2<<" / "<<avgs[i].exp <<") - "<<"("<<avgs[i].m<<"*"<<avgs[i].m<<" / "<<"("<<avgs[i].exp<<"*"<<avgs[i].exp<<"))"<< std::endl;
		   std::cout << "xi[i] /= " << Temperatures[i] << "*" << lat.Nspins << std::endl;
		   std::cout <<"rs[i] /= (3.0L*" <<lat.L<<" * "<<lat.L<<" * "<<avgs[i].exp<<")" << std::endl;
		   */
	}
	for (int i = 0;i< N_temps; ++i){
		printOutput(lat,Temperatures[i],avgs[i],
				b[i],dbdt[i],xi[i],c[i]);
	}
	if (expCorr != 0.0L){
		setMaxE(lat.L,maxTotE);
	}
}
