//This program performs montecarlo with the Metropolis algorithm simulation of the 3D XY model at the critical temperature
//1/Tc = 0.45416
//taking the system size L as input and outputting binder parameter, db/dt and xi
//
#include <iostream>
#include <cmath>
#include <random>
#include <functional>
#include <sys/syscall.h>
#include <unistd.h>
#include <linux/random.h>
#include <iomanip>
#include <utility>

using namespace std;

//print the lattice
void printLattice(double***lattice,double&L){
	cout << "//////////////////" << endl;
	for (int i = 0; i<L; ++i){
		for (int j = 0; j<L; ++j){
			for (int k = 0; k<L; ++k){
				cout << lattice[i][j][k] << " ";
			}
			cout << endl;
		}
		cout << endl;
	}
}


//calculates the energy of a site
double siteEnergy(double *** lattice,double &L, int &s1, int &s2, int &s3,double&angle){
	double sum = 0;
	//find indices of neighbours
	int n1m = (s1 -1 + (int)L )%(int)L;
	int n1p = (s1 +1 + (int)L )%(int)L;
	int n2m = (s2 -1 + (int)L )%(int)L;
	int n2p = (s2 +1 + (int)L )%(int)L;
	int n3m = (s3 -1 + (int)L )%(int)L;
	int n3p = (s3 +1 + (int)L )%(int)L;
	sum -= cos(angle-lattice[n1m][s2][s3]);
	sum -= cos(angle-lattice[n1p][s2][s3]);
	sum -= cos(angle-lattice[s1][n2m][s3]);
	sum -= cos(angle-lattice[s1][n2p][s3]);
	sum -= cos(angle-lattice[s1][s2][n3m]);
	sum -= cos(angle-lattice[s1][s2][n3p]);
	return sum;
}
//calculate sin(theta - theta_x) upwards +, downward -
double sinX(double ***lattice,double &L, int &s1, int &s2, int &s3,double &angle){
	int np = (s1 + 1) %(int)L;
	int nm = (s1 -1 + (int)L) % (int)L;	
	double ret = 0;
	ret = sin(lattice[nm][s2][s3] - angle) + sin(angle - lattice[np][s2][s3]);
	return ret;
}


//testing functions
double calcSinX(double ***lattice,double &L){
	double sum = 0;
	for (int i =0; i< L; ++i){
		for (int j =0; j< L ; ++j){
			for (int k = 0; k<L; ++k){
				sum += sin(lattice[i][j][k] - lattice[(i+1)%(int)L][j][k]);
			}
		}
	}
	return sum;
}
double calcXMag(double ***lattice,double&L){
	double ret = 0;
	for (int i = 0; i<L; ++i){
		for (int j = 0; j<L; ++j){
			for (int k = 0; k<L; ++k){
				ret += cos(lattice[i][j][k]);
			}
		}
	}
	return ret;
}
double calcYMag(double ***lattice,double&L){
	double ret = 0;
	for (int i = 0; i<L; ++i){
		for (int j = 0; j<L; ++j){
			for (int k = 0; k<L; ++k){
				ret += sin(lattice[i][j][k]);
			}
		}
	}
	return ret;
}

double calcMag(double ***lattice,double&L){
	double mag = sqrt(pow(calcXMag(lattice,L),2) + pow(calcYMag(lattice,L),2));
	return mag;
}	

double calcEn(double ***lattice,double&L){
	double en = 0;
	for (int i = 0; i< L; ++i){
		for (int j = 0; j< L; ++j){
			for (int k = 0; k<L; ++k){	
				en += siteEnergy(lattice,L,i,j,k,lattice[i][j][k]);
			}
		}
	}
	en = 0.5*en;
	return en;
}

void sweep(double***lattice,double&L,double&beta,double&TotXMag,double&TotYMag,double&TotEn,double &TotSinX,auto &randgen){
	double prob;
	double u;
	int s1;
	int s2;
	int s3;
	double angleBefore;
	double angleAfter;
	double enBefore;
	double enAfter;
	for (int i = 0; i<(L*L*L); ++i){
		//select random angle in the range [-PI,PI]
		u = -M_PI + 2*M_PI*randgen(); 
		//select random spin
		s1 = L*randgen();
		s2 = L*randgen();
		s3 = L*randgen();
		//calculate energy difference and probability of flipping
		//and try to flip
		angleBefore = lattice[s1][s2][s3];
		angleAfter = angleBefore + u;
		enBefore = siteEnergy(lattice,L,s1,s2,s3,angleBefore);
		enAfter = siteEnergy(lattice,L,s1,s2,s3,angleAfter);
		prob = exp(-beta*(enAfter - enBefore));
		if (randgen() < prob){
			lattice[s1][s2][s3] = angleAfter;
			TotEn += enAfter - enBefore;
			TotXMag += cos(angleAfter) - cos(angleBefore);
			TotYMag += sin(angleAfter) - sin(angleBefore);
			TotSinX += sinX(lattice,L,s1,s2,s3,angleAfter) - sinX(lattice,L,s1,s2,s3,angleBefore);
		}
	}
}

//main
int main(int argc, char* argv[]){
	//set precision of cout
	cout.precision(17);

	//generate random seed from system and initialize random number generator
	unsigned long int s;
	syscall(SYS_getrandom,&s,sizeof(unsigned long int),0);	
	uniform_real_distribution<double> dist(0,1);
	mt19937_64 eng; 
	eng.seed(s);
	auto randgen = bind(dist,eng);

	//set system size and temperature from input arguments
	if (argc < 2){
		cout << "input arguments: L T M_init N_equil N_samp" << endl;
		exit(0);
	}
	//system size
	double L = stod(argv[1]);
	//temperature
	double T = stod(argv[2]);
	double beta = 1.0/T;
	//initial configuration
	double init = stod(argv[3]);
	//number of equilibration sweeps
	double N_equil_sweeps = L*stod(argv[4]);
	//number of samples
	double Nsamples = L*stod(argv[5]);

	double TotEn;
	double TotXMag;
	double TotYMag;
	double TotMag;
	double TotSinX;

	//define and initialize the lattice and cluster
	double ***lattice;
	bool***cluster;
	lattice = new double **[(int)L];
	for (int i = 0; i< L;++i){
		lattice[i] = new double *[(int)L];
		for (int j =0;j<L;++j){
			lattice[i][j] = new double[(int)L];
		}
	}
	if (init == 0){
	for (int i = 0; i<L;++i){
		for (int j=0; j<L;++j){
			for (int k = 0; k<L; ++k){
				lattice[i][j][k] = 2*M_PI*randgen();
			}
		}
	}
	}
	else{
	for (int i = 0; i<L;++i){
		for (int j=0; j<L;++j){
			for (int k = 0; k<L; ++k){
				lattice[i][j][k] = M_PI;
			}
		}
	}
	}

	TotEn = calcEn(lattice,L); 
	TotXMag = calcXMag(lattice,L);
	TotYMag = calcYMag(lattice,L);
	TotSinX = calcSinX(lattice,L);
	//test if energy and mag matches
	/*
	   TotMag = sqrt(pow(TotXMag,2) + pow(TotYMag,2));
	   double testEn = calcEn(lattice,L);
	   double testXMag = calcXMag(lattice,L);
	   double testYMag = calcYMag(lattice,L);
	   double testMag = calcMag(lattice,L);
	   cout << TotEn <<" TotEn vs testEn " << testEn << endl;
	   cout << TotXMag <<" TotXMag vs testXMag " << testXMag << endl;
	   cout << TotYMag <<" TotYMag vs testYMag " << testYMag << endl;
	   cout << TotMag <<" TotMag vs testMag " << testMag << endl;
	   */

	//eqilibration sweeps
	for (int t=0; t < N_equil_sweeps; ++t){
		sweep(lattice,L,beta,TotXMag,TotYMag,TotEn,TotSinX,randgen);
	}

	//test if matches after equilibration
	/*
	double tSinx = calcSinX(lattice,L);
	cout << tSinx << " " << TotSinX << endl;
	*/
	/*
	   testEn = calcEn(lattice,L);
	   testXMag = calcXMag(lattice,L);
	   testYMag = calcYMag(lattice,L);
	   testMag = calcMag(lattice,L);
	   TotMag = sqrt(pow(TotYMag,2) + pow(TotXMag,2));
	   cout << TotEn <<" TotEn vs testEn " << testEn << endl;
	   cout << TotXMag <<" TotXMag vs testXMag " << testXMag << endl;
	   cout << TotYMag <<" TotYMag vs testYMag " << testYMag << endl;
	   cout << TotMag <<" TotMag vs testMag " << testMag << endl;
	   */
	//start collecting data

	//parameters and physical quantities
	//averages
	double avgE = 0; //energy
	double avgE2 = 0;//squared energy
	double avgM = 0; //abs of magnetization
	double avgM2 = 0;//squared magnetization
	double avgM4 = 0;//fourth power of magnetization
	double avgM2E = 0;// squared magnetization times energy
	double avgM4E = 0; // 4th power magnetization times energy

	double avgSinX2 = 0;



	double xi = 0;//susceptibility
	double b = 0; //Binder parameter
	double dbdt = 0;//derivative wrt T of Binder parameter
	double rs = 0;//superfluid density

	for ( int i = 0; i < Nsamples; ++i){
		//perform 2 sweeps between taking data
		sweep(lattice,L,beta,TotXMag,TotYMag,TotEn,TotSinX,randgen);
		sweep(lattice,L,beta,TotXMag,TotYMag,TotEn,TotSinX,randgen);
		//take sample data
		avgE += TotEn;
		avgE2 += TotEn*TotEn;
		avgM += sqrt(TotXMag*TotXMag + TotYMag*TotYMag);
		avgM2 += TotXMag*TotXMag + TotYMag*TotYMag;
		avgM4 += (TotXMag*TotXMag + TotYMag*TotYMag)*(TotXMag*TotXMag + TotYMag*TotYMag);
		avgM2E +=(TotXMag*TotXMag + TotYMag*TotYMag)*TotEn;
		avgM4E += (TotXMag*TotXMag + TotYMag*TotYMag)*(TotXMag*TotXMag + TotYMag*TotYMag)*TotEn;

		avgSinX2 += TotSinX*TotSinX;
	}

	//calculate quantities of interest
	

	//normalize

	avgE /= Nsamples;
	avgE2 /= Nsamples;
	avgM /= Nsamples;
	avgM2 /= Nsamples;
	avgM4 /= Nsamples;
	avgM2E /= Nsamples;
	avgM4E /= Nsamples;
	avgSinX2 /= Nsamples;

	//calculate
	b = avgM4;
	b /= (avgM2*avgM2);
	dbdt = (avgM4E/(avgM2*avgM2) + 2.0*avgM4*avgE/(avgM2*avgM2) - 3.0*avgM4*avgM2E/(avgM2*avgM2*avgM2));
	dbdt /= (T)*(T);
	xi = avgM2 - avgM*avgM;
	xi /= L*L*L*(T);
	rs = -(1.0/3.0)*avgE - beta*avgSinX2;
	rs /= L*L;
	//get energy and mag per spin instead
	avgE /= L*L*L;
	avgM /= L*L*L;

	//print to terminal
	cout << fixed << L << " ";
	cout << fixed << T << " ";
	cout << fixed << avgE << " ";
	cout << fixed << avgM << " ";
	cout << fixed << b << " ";
	cout << fixed << dbdt << " ";
	cout << fixed << xi << " ";
	cout << fixed << N_equil_sweeps << " ";
	cout << fixed << rs << " ";
	cout << fixed << endl;
}
