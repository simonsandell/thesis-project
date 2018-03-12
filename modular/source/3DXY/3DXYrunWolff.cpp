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

void wolffHistRun3DXY(Lattice3DXY& lat, long double N_sample_sweeps,long double *Temperatures,int N_temps,long double runTemp){


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
	long double maxTotE = getMaxE3DXY(lat.L); 
	long double expCorr = 0.0L;

	long double steps = 0.0L;
	long double NsampClust = 0.0L;
	long double doneSweeps = 0.0L;

	Cluster cluster(lat.L);
	RandStruct rand;

	while (doneSweeps < N_sample_sweeps){
		//make a cluster
		steps = (long double)cluster3DXY(lat,cluster,Beta,rand);
		doneSweeps += steps/lat.Nspins;
		if (doneSweeps< 0.0L || steps < 0.0L) {
			std::cout << "OVERFLOW" << std::endl;
		}
		NsampClust += 1.0L;

		//update maxE if necessary
		
		if (std::abs(lat.energy) > std::abs(maxTotE)){
			expCorr = 1.0L;
			if (NsampClust > 1.0L){
				expCorr = exp(-maxTotE +lat.energy);	
				for (int k = 0; k<N_temps;++k){
					avgs[k].e     *= expCorr;
					avgs[k].e2     *= expCorr;
					avgs[k].m     *= expCorr;
					avgs[k].m2     *= expCorr;
					avgs[k].m4     *= expCorr;
					avgs[k].m2e     *= expCorr;
					avgs[k].m4e     *= expCorr;
					avgs[k].s2x     *= expCorr;
					avgs[k].s2y     *= expCorr;
					avgs[k].s2z     *= expCorr;
					avgs[k].exp     *= expCorr;
				}
			}
			maxTotE = lat.energy;
		}
		//take sample data
		long double tE;
		long double tM2;
		long double tSx;
		long double tSy;
		long double tSz;
		for (int i = 0; i<N_temps; ++i){
			expFac = exp(-(Betas[i] - Beta)*(lat.energy-maxTotE));
			avgs[i].exp += expFac;

			tE = lat.energy/lat.Nspins;
			tM2 = lat.xmag*lat.xmag + lat.ymag*lat.ymag;
			tM2 /= lat.Nspins*lat.Nspins;
			tSx = lat.sinx/lat.Nspins;
			tSy = lat.siny/lat.Nspins;
			tSz = lat.sinz/lat.Nspins;

			avgs[i].e += expFac*tE;
			avgs[i].e2+=expFac*tE*tE;
			avgs[i].m += expFac*sqrt(tM2);
			avgs[i].m2 += expFac*tM2;
			avgs[i].m4 += expFac*tM2*tM2;
			avgs[i].m2e += expFac*tM2*tE; 
			avgs[i].m4e += expFac*tM2*tM2*tE;
			avgs[i].s2x += expFac*tSx*tSx;
			avgs[i].s2y += expFac*tSy*tSy;
			avgs[i].s2z += expFac*tSz*tSz;
		}
	}//end of samples
	lat.Nsmclusts=NsampClust; 
	lat.Nsmsweeps = doneSweeps;




	//calculate quantities of interest

	long double xi[N_temps];//susceptibility
	long double b[N_temps]; //Binder parameter
	long double dbdt[N_temps];//derivative wrt T of Binder parameter
	long double rs[N_temps];//superfluid density
	for (int i =0; i< N_temps; ++i){

		//print values
		/*
		   std::cout <<"avgExpFac[i]"<<	avgExpFac[i]<<std::endl;
		   std::cout <<"avgE[i]     "<<        avgE[i] <<std::endl;
		   std::cout <<"avgE2[i]    "<<        avgE2[i]  <<std::endl;
		   std::cout <<"avgM[i]     "<<        avgM[i] <<std::endl;
		   std::cout <<"avgM2[i]    "<<        avgM2[i]<<std::endl;
		   std::cout <<"avgM4[i]    "<<        avgM4[i] <<std::endl;
		   std::cout <<"avgM2E[i]   "<<        avgM2E[i]<<std::endl;
		   std::cout <<"avgM4E[i]   "<<        avgM4E[i]<<std::endl;
		   std::cout <<"avgs[i].s2x "<<        avgs[i].s2x <<std::endl;
		   std::cout <<"avgSinY2[i] "<<        avgSinY2[i] <<std::endl;
		   std::cout <<"avgs[i].s2z "<<        avgs[i].s2z <<std::endl;
		   */

		//normalize
		avgs[i].e   /= NsampClust;
		avgs[i].e2  /= NsampClust;
		avgs[i].m   /= NsampClust;
		avgs[i].m2  /= NsampClust;
		avgs[i].m4  /= NsampClust;
		avgs[i].m2e /= NsampClust;
		avgs[i].m4e /= NsampClust;
		avgs[i].s2x /= NsampClust;
		avgs[i].s2y /= NsampClust;
		avgs[i].s2z /= NsampClust;
		avgs[i].exp /= NsampClust;

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
		//print values
		/*
		   std::cout << "b = " << avgs[i].m4 << " * " << avgs[i].exp << std::endl;
		   std::cout << "b /= " << avgs[i].m2 << " * " << avgs[i].m2 << std::endl;
		   std::cout << "dbdt[i] = " << avgs[i].exp << " * " << avgs[i].m4e << 
		   " * " << avgs[i].m2<<" + "<< avgs[i].m4<< " * " <<avgs[i].m2<< 
		   " * " << avgs[i].e << " - 2.0L* " << avgs[i].exp<< " * " <<
		   avgs[i].m4 << " * " << avgs[i].m2e << std::endl;
		   std::cout << "dbdt[i] /= " << Temperatures[i] << "^2 * " << avgM2 << "^3" << std::endl;
		   std::cout << "xi[i] = " << " ( " << avgs[i].m2<<" / "<<avgs[i].exp <<") - "<<"("<<avgs[i].m<<"*"<<avgs[i].m<<" / "<<"("<<avgs[i].exp<<"*"<<avgs[i].exp<<"))"<< std::endl;
		   std::cout << "xi[i] /= " << Temperatures[i] << "*" << lat.Nspins << std::endl;
		   std::cout <<"rs[i] = -"<<avgs[i].e <<" - "<< avgs[i].s2x<<" / "<<Temperatures[i] 
		   <<" - "<<avgs[i].s2y<<" / "<<Temperatures[i] 
		   <<" - "<<avgs[i].s2z<<" / "<<Temperatures[i] << std::endl;
		   std::cout <<"rs[i] /= (3.0L*" <<lat.L<<" * "<<lat.L<<" * "<<avgs[i].exp<<")" << std::endl;
		   */
	}
	for (int i = 0;i< N_temps; ++i){
		print3DXYOutput(lat,Temperatures[i],avgs[i],
				b[i],dbdt[i],xi[i],rs[i]);
	}
	if (expCorr != 0.0L){
		setMaxE3DXY(lat.L,maxTotE);
	}
}
