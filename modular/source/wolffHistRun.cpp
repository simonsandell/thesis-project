
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

void wolffHistRun(long double L,long double ***lattice,long double Neq_sweeps,long double Neq_clusts, long double N_sample_sweeps,bool cold,long double *Temperatures,int N_temps,long double runTemp){

	//initialize rng
	unsigned long int s;
	syscall(SYS_getrandom,&s,sizeof(unsigned long int),0);	
	std::uniform_real_distribution<long double> dist(0.0L,1.0L);
	std::mt19937_64 eng; 
	eng.seed(s);

	//convert temp to betas
	long double Betas[N_temps];	
	for (int i = 0; i< N_temps; ++i){
		Betas[i] = 1.0L/Temperatures[i];
	}
	long double Temperature = runTemp;
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


	long double avgE[N_temps] = {}; //energy
	long double avgE2[N_temps] = {};//squared energy
	long double avgM[N_temps] = {}; //abs of magnetization
	long double avgM2[N_temps] = {};//squared magnetization
	long double avgM4[N_temps] = {};//fourth power of magnetization
	long double avgM2E[N_temps] = {};// squared magnetization times energy
	long double avgM4E[N_temps] = {}; // 4th power magnetization times energy
	long double avgSinX2[N_temps] = {}; // for superfluid density 
	long double avgSinY2[N_temps] = {}; // for superfluid density 
	long double avgSinZ2[N_temps] = {}; // for superfluid density 
	long double avgExpFac[N_temps] = {};
	long double expFac;



	long double maxTotE = getMaxE(L); 
	long double expCorr = 0.0L;

	int steps = 0;
	int Nsample_clusts = 0;
	long double leaststeps = N_sample_sweeps*L*L*L;
	while (steps < leaststeps){
		//make a cluster
		steps += growCluster(lattice,cluster,L,Beta,
				TotXMag,TotYMag,TotEn,TotSinX,TotSinY,TotSinZ,
				dist,eng);

		++Nsample_clusts;

		//update maxE if necessary
		
		if (std::abs(TotEn) > std::abs(maxTotE)){
			expCorr = 1.0L;
			if (Nsample_clusts > 1){
				expCorr = exp(-maxTotE +TotEn);	
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
			maxTotE = TotEn;
		}
		//take sample data
		for (int i = 0; i<N_temps; ++i){
			expFac = exp(-(Betas[i] - Beta)*(TotEn-maxTotE));
			avgExpFac[i] += expFac;
			avgE[i] += expFac*TotEn;
			avgE2[i] += expFac*TotEn*TotEn;
			avgM[i] += expFac*sqrt(TotXMag*TotXMag + TotYMag*TotYMag);
			avgM2[i] += expFac*(TotXMag*TotXMag + TotYMag*TotYMag);
			avgM4[i] += expFac*(TotXMag*TotXMag + TotYMag*TotYMag)*(TotXMag*TotXMag + TotYMag*TotYMag);
			avgM2E[i] += TotEn*expFac*(TotXMag*TotXMag + TotYMag*TotYMag); 
			avgM4E[i] += TotEn*expFac*(TotXMag*TotXMag + TotYMag*TotYMag)*(TotXMag*TotXMag + TotYMag*TotYMag);
			avgSinX2[i] += TotSinX*TotSinX*expFac;
			avgSinY2[i] += TotSinY*TotSinY*expFac;
			avgSinZ2[i] += TotSinZ*TotSinZ*expFac;
		}
	}
	long double actNsamp_sweeps = (long double)steps/(L*L*L);

<<<<<<< HEAD
=======
	//define some reciprocals to reduce number of divions
>>>>>>> restored

	//calculate quantities of interest

	long double xi[N_temps] = {};//susceptibility
	long double b[N_temps] = {}; //Binder parameter
	long double dbdt[N_temps] = {};//derivative wrt T of Binder parameter
	long double rs[N_temps] = {};//superfluid density
	for (int i =0; i< N_temps; ++i){


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

<<<<<<< HEAD
=======
//		avgE[i] *= reciExpFac;
//		avgE2[i] *= reciExpFac;
//		avgM[i] *= reciExpFac;
//		avgM2[i] *= reciExpFac;
//		avgM4[i] *= reciExpFac;
//		avgM2E[i] *= reciExpFac;
//		avgM4E[i] *= reciExpFac;
//		avgSinX2[i] *= reciExpFac;
//		avgSinY2[i] *= reciExpFac;
//		avgSinZ2[i] *= reciExpFac;
>>>>>>> restored
		//calculate
		b[i] = avgM4[i]*avgExpFac[i];
		b[i] /= (avgM2[i]*avgM2[i]);
		dbdt[i] = avgExpFac[i]*avgM4E[i]*avgM2[i] 
			+ avgM4[i]*avgM2[i]*avgE[i] 
			- 2.0L*avgExpFac[i]*avgM4[i]*avgM2E[i];
		dbdt[i] /= Temperatures[i]*Temperatures[i]*avgM2[i]*avgM2[i]*avgM2[i];
		xi[i] = (avgM2[i]/avgExpFac[i]) -
		       	(avgM[i]*avgM[i]/(avgExpFac[i]*avgExpFac[i]));
		xi[i] /= (Temperatures[i]*L*L*L);
		rs[i] = -avgE[i] - avgSinX2[i]/Temperatures[i] 
			-avgSinY2[i]/Temperatures[i] 
			-avgSinZ2[i]/Temperatures[i];
		rs[i] /= (3.0L*L*L*avgExpFac[i]);
	}
	for (int i = 0;i< N_temps; ++i){
		printOutput(L,Temperatures[i],
				Neq_sweeps,Neq_clusts,
				actNsamp_sweeps,Nsample_clusts,cold,
				avgE[i],avgE2[i],avgM[i],avgM2[i],avgM4[i],
				avgM2E[i],avgM4E[i],
				avgSinX2[i],avgSinY2[i],avgSinZ2[i],
				b[i],dbdt[i],xi[i],rs[i],
				avgExpFac[i]);
	}
	if (expCorr != 0.0L){
		setMaxE(L,maxTotE);
	}
}
