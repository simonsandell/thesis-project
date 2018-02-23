
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
#include "clusterStruct.h"
#include "randStruct.h"

void wolffHistRun(Lattice& lat, long double N_sample_sweeps,long double *Temperatures,int N_temps,long double runTemp){


	//convert temp to betas
	long double Betas[N_temps];	
	for (int i = 0; i< N_temps; ++i){
		Betas[i] = 1.0L/Temperatures[i];
	}
	long double Beta = 1.0L/runTemp;		


	//update lattice quantities
	
	lat.updateQuants();

	long double avgE[N_temps]; //energy
	long double avgE2[N_temps];//squared energy
	long double avgM[N_temps]; //abs of magnetization
	long double avgM2[N_temps];//squared magnetization
	long double avgM4[N_temps];//fourth power of magnetization
	long double avgM2E[N_temps];// squared magnetization times energy
	long double avgM4E[N_temps]; // 4th power magnetization times energy
	long double avgSinX2[N_temps]; // for superfluid density 
	long double avgSinY2[N_temps]; // for superfluid density 
	long double avgSinZ2[N_temps]; // for superfluid density 
	long double avgExpFac[N_temps];
	for (int i = 0; i< N_temps; ++i){
		avgE[i]=0; 
                avgE2[i]=0;
                avgM[i]=0;
                avgM2[i]=0;
                avgM4[i]=0;
                avgM2E[i]=0;
                avgM4E[i]=0;
                avgSinX2[i]=0; 
                avgSinY2[i]=0; 
                avgSinZ2[i]=0; 
                avgExpFac[i]=0;
	}
	long double expFac = 0.0L;
	long double maxTotE = getMaxE(lat.L); 
	long double expCorr = 0.0L;

	int steps = 0;
	int Nsample_clusts = 0;
	long double leaststeps = N_sample_sweeps*lat.Nspins;

	Cluster cluster(lat.L);
	RandStruct rand;

	while (steps < leaststeps){
		//make a cluster
		steps += growCluster(lat,cluster,Beta,rand);

		++Nsample_clusts;

		//update maxE if necessary
		
		if (std::abs(lat.energy) > std::abs(maxTotE)){
			expCorr = 1.0L;
			if (Nsample_clusts > 1){
				expCorr = exp(-maxTotE +lat.energy);	
				for (int k = 0; k<N_temps;++k){
					avgExpFac[k] *= expCorr;
					avgE[k] *= expCorr;
					avgE2[k] *= expCorr;
					avgM[k] *= expCorr;
					avgM2[k] *= expCorr;
					avgM4[k] *= expCorr;
					avgM2E[k] *= expCorr;
					avgM4E[k] *= expCorr;
					avgSinX2[k] *= expCorr;
					avgSinY2[k] *= expCorr;
					avgSinZ2[k] *= expCorr;
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
			avgExpFac[i] += expFac;
			
			tE = lat.energy/lat.Nspins;
			tM2 = lat.xmag*lat.xmag + lat.ymag*lat.ymag;
			tM2 /= lat.Nspins*lat.Nspins;
			tSx = lat.sinx/lat.Nspins;
			tSy = lat.siny/lat.Nspins;
			tSz = lat.sinz/lat.Nspins;

			avgE[i] += expFac*tE;
			avgE2[i] += expFac*tE*tE;
			avgM[i] += expFac*sqrt(tM2);
			avgM2[i] += expFac*tM2;
			avgM4[i] += expFac*tM2*tM2;
			avgM2E[i] += expFac*tM2*tE; 
			avgM4E[i] += expFac*tM2*tM2*tE;
			avgSinX2[i] += expFac*tSx;
			avgSinY2[i] += expFac*tSy;
			avgSinZ2[i] += expFac*tSz;
		}
	}//end of samples
	lat.Nsmclusts=Nsample_clusts; 
	lat.Nsmsweeps = ((long double)steps)/((long double)lat.Nspins);




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
        	std::cout <<"avgSinX2[i] "<<        avgSinX2[i] <<std::endl;
        	std::cout <<"avgSinY2[i] "<<        avgSinY2[i] <<std::endl;
        	std::cout <<"avgSinZ2[i] "<<        avgSinZ2[i] <<std::endl;
		*/

		//normalize
		avgExpFac[i] /= Nsample_clusts;
		avgE[i] /= Nsample_clusts;
		avgE2[i] /= Nsample_clusts;
		avgM[i] /= Nsample_clusts;
		avgM2[i] /= Nsample_clusts;
		avgM4[i] /= Nsample_clusts;
		avgM2E[i] /= Nsample_clusts;
		avgM4E[i] /= Nsample_clusts;
		avgSinX2[i] /= Nsample_clusts;
		avgSinY2[i] /= Nsample_clusts;
		avgSinZ2[i] /= Nsample_clusts;

		//calculate
		b[i] = avgM4[i]*avgExpFac[i];
		b[i] /= (avgM2[i]*avgM2[i]);
		dbdt[i] = avgExpFac[i]*avgM4E[i]*avgM2[i] 
			+ avgM4[i]*avgM2[i]*avgE[i] 
			- 2.0L*avgExpFac[i]*avgM4[i]*avgM2E[i];
		dbdt[i] *= lat.Nspins;
		dbdt[i] /= Temperatures[i]*Temperatures[i]*avgM2[i]*avgM2[i]*avgM2[i];
		xi[i] = ((avgM2[i]/avgExpFac[i]) -
		       	(avgM[i]*avgM[i]/(avgExpFac[i]*avgExpFac[i])))*lat.Nspins;
		xi[i] /= (Temperatures[i]);
		rs[i] = -avgE[i] - avgSinX2[i]/Temperatures[i] 
			-avgSinY2[i]/Temperatures[i] 
			-avgSinZ2[i]/Temperatures[i];
		rs[i] *= lat.L;
		rs[i] /= (3.0L*avgExpFac[i]);
		//print values
		/*
		std::cout << "b = " << avgM4[i] << " * " << avgExpFac[i] << std::endl;
		std::cout << "b /= " << avgM2[i] << " * " << avgM2[i] << std::endl;
		std::cout << "dbdt[i] = " << avgExpFac[i] << " * " << avgM4E[i] << 
			" * " << avgM2[i]<<" + "<< avgM4[i]<< " * " <<avgM2[i]<< 
			" * " << avgE[i] << " - 2.0L* " << avgExpFac[i]<< " * " <<
		       	avgM4[i] << " * " << avgM2E[i] << std::endl;
		std::cout << "dbdt[i] /= " << Temperatures[i] << "^2 * " << avgM2 << "^3" << std::endl;
		std::cout << "xi[i] = " << " ( " << avgM2[i]<<" / "<<avgExpFac[i] <<") - "<<"("<<avgM[i]<<"*"<<avgM[i]<<" / "<<"("<<avgExpFac[i]<<"*"<<avgExpFac[i]<<"))"<< std::endl;
		std::cout << "xi[i] /= " << Temperatures[i] << "*" << lat.Nspins << std::endl;
		std::cout <<"rs[i] = -"<<avgE[i] <<" - "<< avgSinX2[i]<<" / "<<Temperatures[i] 
			<<" - "<<avgSinY2[i]<<" / "<<Temperatures[i] 
			<<" - "<<avgSinZ2[i]<<" / "<<Temperatures[i] << std::endl;
		std::cout <<"rs[i] /= (3.0L*" <<lat.L<<" * "<<lat.L<<" * "<<avgExpFac[i]<<")" << std::endl;
		*/
	}
	for (int i = 0;i< N_temps; ++i){
		printOutput(lat,Temperatures[i],				
				avgE[i],avgE2[i],avgM[i],avgM2[i],avgM4[i],
				avgM2E[i],avgM4E[i],
				avgSinX2[i],avgSinY2[i],avgSinZ2[i],
				b[i],dbdt[i],xi[i],rs[i],
				avgExpFac[i]);
	}
	if (expCorr != 0.0L){
		setMaxE(lat.L,maxTotE);
	}
}
