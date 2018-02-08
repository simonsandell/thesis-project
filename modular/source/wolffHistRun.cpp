
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

void wolffHistRun(long double L, long double N_equil_sweeps, long double N_samples,bool cold,long double *Temperatures,int N_temps,long double runTemp){

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
	//define some reciprocals to reduce number of divions
	long double reciNsamples = 1.0L/N_samples;
	long double reciNspins = 1.0L/(L*L*L);

	//initialize lattice
	long double *** lattice = newLattice(L,cold,dist,eng);

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

	//Set equilibration time 
	long double N_equil_steps= N_equil_sweeps*L*L*L;
	//eqilibration 
	int totEqSteps= 0;
	int eqClusts =0;
	while (totEqSteps < N_equil_steps){
		eqClusts++;
		totEqSteps += growCluster(lattice,cluster,L,Beta,TotXMag,TotYMag,TotEn,TotSinX,TotSinY,TotSinZ,dist,eng);
	}
	long double eqSweeps = ((long double)totEqSteps)*reciNspins;

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

	for ( int j = 0; j < N_samples; ++j){
		//make a cluster
		growCluster(lattice,cluster,L,Beta,TotXMag,TotYMag,TotEn,TotSinX,TotSinY,TotSinZ,dist,eng);

		//update maxE if necessary
		if (std::abs(TotEn) > std::abs(maxTotE)){
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


	//calculate quantities of interest
	long double reciExpFac = 0.0L;

	long double Eps[N_temps] = {};//energy per spin
	long double Mps[N_temps] = {};//magnetization per spin
	long double xi[N_temps] = {};//susceptibility
	long double b[N_temps] = {}; //Binder parameter
	long double dbdt[N_temps] = {};//derivative wrt T of Binder parameter
	long double rs[N_temps] = {};//superfluid density
	for (int i =0; i< N_temps; ++i){


		//normalize
		avgExpFac[i] *= reciNsamples;
		reciExpFac = 1.0L/avgExpFac[i];
		avgE[i] *= reciNsamples;
		avgE2[i] *= reciNsamples;
		avgM[i] *= reciNsamples;
		avgM2[i] *= reciNsamples;
		avgM4[i] *= reciNsamples;
		avgM2E[i] *= reciNsamples;
		avgM4E[i] *= reciNsamples;
		avgSinX2[i] *= reciNsamples;
		avgSinY2[i] *= reciNsamples;
		avgSinZ2[i] *= reciNsamples;

		avgE[i] *= reciExpFac;
		avgE2[i] *= reciExpFac;
		avgM[i] *= reciExpFac;
		avgM2[i] *= reciExpFac;
		avgM4[i] *= reciExpFac;
		avgM2E[i] *= reciExpFac;
		avgM4E[i] *= reciExpFac;
		avgSinX2[i] *= reciExpFac;
		avgSinY2[i] *= reciExpFac;
		avgSinZ2[i] *= reciExpFac;
		//calculate
		b[i] = avgM4[i];
		b[i] /= (avgM2[i]*avgM2[i]);
		dbdt[i] = avgM4E[i]*avgM2[i] + avgM4[i]*avgM2[i]*avgE[i] - 2.0L*avgM4[i]*avgM2E[i];
		dbdt[i] *= Betas[i]*Betas[i];
		dbdt[i] /= avgM2[i]*avgM2[i]*avgM2[i];
		xi[i] = avgM2[i] - avgM[i]*avgM[i];
		xi[i] *= reciNspins;
		xi[i] *= Betas[i];
		rs[i] = -avgE[i] - (Betas[i])*avgSinX2[i] -(Betas[i])*avgSinY2[i] -(Betas[i])*avgSinZ2[i];
		rs[i] *= (1.0L/3.0L)*L*reciNspins; 

		Eps[i] = avgE[i]*reciNspins;
		Mps[i] = avgM[i]*reciNspins;
	}
	for (int i = 0;i< N_temps; ++i){
		printOutput(L,Temperatures[i],Eps[i],Mps[i],b[i],dbdt[i],xi[i],rs[i],eqSweeps,eqClusts,cold);

	}
	if (expCorr != 0.0L){
		setMaxE(L,maxTotE);
	}
}
