//This program performs montecarlo with the Wolff algorithm simulation of the 3D XY model at the critical temperature
//1/Tc = 0.45416
//taking the system size L as input and outputting binder parameter, db/dt and xi
//
//Implements histogramextrapolation to obtain values at different temperatures
#include <iostream>
#include <cmath>
#include <random>
#include <functional>
#include <sys/syscall.h>
#include <unistd.h>
#include <linux/random.h>
#include <iomanip>
#include <utility>
#include <tuple>

using namespace std;

void printLattice(double ***lattice,double &L){
	for(int i = 0; i < L; ++i){
		for(int j = 0; j < L; ++j){
			for(int k =0; k<L; ++k){
				cout << lattice[i][j][k];
			}
			cout << endl;
		}
		cout << endl;
	}
}

//clear the cluster
void emptyCluster(bool***cluster,double &L){
	int steps = 0;
	for (int i = 0; i< L; ++i){
		for (int j = 0; j< L; ++j){
			for (int k = 0; k<L; ++k){	
				cluster[i][j][k] = 0;
			}
		}
	}
}

//calc product of two spins
double innerProd(double &angle1,double &angle2){
	double prod = cos(angle1 - angle2);
	return prod;
}

//reflect spin 
double rSpin(double&u,double&spin){
	double ret = M_PI + 2*u -spin;
	ret = ret + 4*M_PI;
	ret = fmod(ret,2*M_PI);
	return ret;
}

//calculate energy of site
double siteEnergy(double *** lattice,double &L, int &s1, int &s2, int &s3){
	double sum = 0;
	//find indices of neighbours
	int n1m = (s1 -1 + (int)L )%(int)L;
	int n1p = (s1 +1 + (int)L )%(int)L;
	int n2m = (s2 -1 + (int)L )%(int)L;
	int n2p = (s2 +1 + (int)L )%(int)L;
	int n3m = (s3 -1 + (int)L )%(int)L;
	int n3p = (s3 +1 + (int)L )%(int)L;
	sum -= innerProd(lattice[s1][s2][s3],lattice[n1m][s2][s3]);
	sum -= innerProd(lattice[s1][s2][s3],lattice[n1p][s2][s3]);
	sum -= innerProd(lattice[s1][s2][s3],lattice[s1][n2m][s3]);
	sum -= innerProd(lattice[s1][s2][s3],lattice[s1][n2p][s3]);
	sum -= innerProd(lattice[s1][s2][s3],lattice[s1][s2][n3m]);
	sum -= innerProd(lattice[s1][s2][s3],lattice[s1][s2][n3p]);
	return sum;
}

double freezingProb(double ***lattice,double&L,double&beta,double &u,double &S1,double &S2){
	double prob = 1 - exp(-2*beta*(innerProd(S1,u))*(innerProd(S2,u)));
	return prob;
}

//testing functions
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
				en += siteEnergy(lattice,L,i,j,k);
			}
		}
	}
	en = 0.5*en;
	return en;
}

//make a cluster..
int growCluster(double &u,int &s1,int &s2,int &s3,double ***lattice,bool ***cluster, double &L,double &beta, auto &randgen,double& TotXMag,double& TotYMag,double& TotEn){
	int time = 1;
	//reflect spin and mark as part of cluster
	// 
	double angleBefore = lattice[s1][s2][s3];
	double enBefore = siteEnergy(lattice,L,s1,s2,s3);
	lattice[s1][s2][s3] = rSpin(u,lattice[s1][s2][s3]);
	cluster[s1][s2][s3] = 1;
	double angleAfter = lattice[s1][s2][s3];
	TotEn += siteEnergy(lattice,L,s1,s2,s3) - enBefore;
	TotXMag += cos(angleAfter) - cos(angleBefore);
	TotYMag += sin(angleAfter) - sin(angleBefore);
	//
	//find indices of nearest neighbours
	int n1m = (s1 -1 + (int)L )%(int)L;
	int n1p = (s1 +1 + (int)L )%(int)L;
	int n2m = (s2 -1 + (int)L )%(int)L;
	int n2p = (s2 +1 + (int)L )%(int)L;
	int n3m = (s3 -1 + (int)L )%(int)L;
	int n3p = (s3 +1 + (int)L )%(int)L;
	//add them to perimeter list
	tuple<int,int,int,double> perimeter[(int)(L*L*L*6)] = {};
	//index at which we want to add another perimeter spin
	//so if it is equal to 0, it means the list is empty
	//consequently the index of the last spin is n-1
	int n = 0;
	perimeter[n] = make_tuple(n1m,s2,s3,angleAfter); n +=1;
	perimeter[n] = make_tuple(n1p,s2,s3,angleAfter); n +=1;
	perimeter[n] = make_tuple(s1,n2m,s3,angleAfter); n +=1;
	perimeter[n] = make_tuple(s1,n2p,s3,angleAfter); n +=1;
	perimeter[n] = make_tuple(s1,s2,n3m,angleAfter); n +=1;
	perimeter[n] = make_tuple(s1,s2,n3p,angleAfter); n +=1;

	tuple<int,int,int,double> current;
	double prob;
	while (n > 0){
		//pick out the last element 
		current = perimeter[n-1];
		n -= 1;

		//test that it is not already part of cluster
		if (cluster[get<0>(current)][get<1>(current)][get<2>(current)] == 0){
			//increase time for every tested spin
			++time;
			//calculate prob of freezing 
			prob = freezingProb(lattice,L,beta,u,get<3>(current),lattice[get<0>(current)][get<1>(current)][get<2>(current)]);
			//add this perimeter spin to the cluster with probability prob
			if (randgen() < prob){
				//save angle and energy before reflecting
				angleBefore = lattice[get<0>(current)][get<1>(current)][get<2>(current)];
				enBefore = siteEnergy(lattice,L,get<0>(current),get<1>(current),get<2>(current));
				//reflect and mark as added to cluster
				lattice[get<0>(current)][get<1>(current)][get<2>(current)] = rSpin(u,lattice[get<0>(current)][get<1>(current)][get<2>(current)]);
				cluster[get<0>(current)][get<1>(current)][get<2>(current)] = 1;
				angleAfter = lattice[get<0>(current)][get<1>(current)][get<2>(current)];
				//update energy and magnetization
				TotEn += siteEnergy(lattice,L,get<0>(current),get<1>(current),get<2>(current)) - enBefore;
				TotXMag += cos(angleAfter) - cos(angleBefore);
				TotYMag += sin(angleAfter) - sin(angleBefore);

				//find indices of its neighbours
				tuple<int,int,int,double> neig1 = make_tuple((get<0>(current) + 1) % (int)L, get<1>(current),get<2>(current),angleBefore);
				tuple<int,int,int,double> neig2 = make_tuple(((int)L + get<0>(current) - 1) % (int)L, get<1>(current),get<2>(current),angleBefore);
				tuple<int,int,int,double> neig3 = make_tuple(get<0>(current), (get<1>(current) + 1) % (int)L,get<2>(current),angleBefore);
				tuple<int,int,int,double> neig4 = make_tuple(get<0>(current), (get<1>(current) + (int)L - 1) % (int)L,get<2>(current),angleBefore);
				tuple<int,int,int,double> neig5 = make_tuple(get<0>(current), get<1>(current), (1 + get<2>(current))%(int)L,angleBefore);
				tuple<int,int,int,double> neig6 = make_tuple(get<0>(current), get<1>(current), (get<2>(current)+(int)L -1 )%(int)L,angleBefore);
				//if it is not already part of the cluster, add it to perimeter list
				if (cluster[get<0>(neig1)][get<1>(neig1)][get<2>(neig1)] ==0){
					perimeter[n] = neig1;
					n = n + 1;
				}
				if (cluster[get<0>(neig2)][get<1>(neig2)][get<2>(neig2)] ==0){
					perimeter[n] = neig2;
					n = n + 1;
				}
				if (cluster[get<0>(neig3)][get<1>(neig3)][get<2>(neig3)] ==0){
					perimeter[n] = neig3;
					n = n + 1;
				}
				if (cluster[get<0>(neig4)][get<1>(neig4)][get<2>(neig4)] ==0){
					perimeter[n] = neig4;
					n = n + 1;
				}
				if (cluster[get<0>(neig5)][get<1>(neig5)][get<2>(neig5)] ==0){
					perimeter[n] = neig5;
					n = n + 1;
				}
				if (cluster[get<0>(neig6)][get<1>(neig6)][get<2>(neig6)] ==0){
					perimeter[n] = neig6;
					n = n + 1;
				}
			}
		}
	}
	return time;
}

//start new cluster
//choose random u vector and starting spin
//grow cluster from those
//empty the cluster when done
//return time  
int newCluster(double *** lattice, bool***cluster,double &L,double &beta,auto &randgen,double& TotXMag,double& TotYMag,double& TotEn){
	double u = 2*M_PI*randgen();
	int s1 = L*randgen();
	int s2 = L*randgen();
	int s3 = L*randgen();
	int time;
	time = growCluster(u,s1,s2,s3,lattice,cluster,L,beta,randgen,TotXMag,TotYMag,TotEn);
	emptyCluster(cluster,L);
	return time;
}

//main
int main(int argc, char* argv[]){
	//generate random seed from system and initialize random number generator
	unsigned long int s;
	syscall(SYS_getrandom,&s,sizeof(unsigned long int),0);	
	uniform_real_distribution<double> dist(0,1);
	mt19937_64 eng; 
	eng.seed(s);
	auto randgen = bind(dist,eng);

	//set system size and temperature from input arguments
	if (argc < 2){
		cout << "input arguments: L T_1 T_2 T_3 ..." << endl;
		exit(0);
	}
	double L = stod(argv[1]);
	double N_temps = 1;
	double *extT;
	if (argc == 2) {
		extT = new double[20];
		double k = 2.101867183371499;
		double dk = 0.01;
		for ( int i = 0; i < 20; ++i){
			extT[i] = k + i*dk;
		}
		N_temps = 20;
	}
	else if (argc> 2){
		extT = new double[argc -2];
		N_temps = argc -2;
		for (int i = 0; i< (argc-2); ++i){
			extT[i] = stod(argv[i+2]);
		}		
	}

	//critical temperature of 3D XY
	double beta = 0.45416;
	double T = 1/0.45416;

	double TotEn;
	double TotXMag;
	double TotYMag;
	double TotMag;

	//
	//Set equilibration time and number of samples
	double N_equil_steps= 300*L*L*L;
	double Nsamples = N_equil_steps; 

	//define and initialize the lattice and cluster
	double ***lattice;
	bool***cluster;
	lattice = new double **[(int)L];
	cluster = new bool**[(int)L];
	for (int i = 0; i< L;++i){
		lattice[i] = new double *[(int)L];
		cluster[i] = new bool*[(int)L];
		for (int j =0;j<L;++j){
			lattice[i][j] = new double[(int)L];
			cluster[i][j] = new bool[(int)L];
		}
	}
	for (int i = 0; i<L;++i){
		for (int j=0; j<L;++j){
			for (int k = 0; k<L; ++k){
				lattice[i][j][k] = 0.5*M_PI;
				cluster[i][j][k] = 0;
			}
		}
	}
	TotEn = -3*L*L*L;
	TotXMag = 0;
	TotYMag = L*L*L; 
	TotMag = L*L*L;
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

	//eqilibration 
	int t = 0;
	while (t < N_equil_steps){
		t += newCluster(lattice,cluster,L,beta,randgen,TotXMag,TotYMag,TotEn);
	}
	//test if matches after equilibration
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
	double avgE[(int)N_temps] = {}; //energy
	double avgE2[(int)N_temps] = {};//squared energy
	double avgM[(int)N_temps] = {}; //abs of magnetization
	double avgM2[(int)N_temps] = {};//squared magnetization
	double avgM4[(int)N_temps] = {};//fourth power of magnetization
	double avgM2E[(int)N_temps] = {};// squared magnetization times energy
	double avgM4E[(int)N_temps] = {}; // 4th power magnetization times energy

	double avgMX2[(int)N_temps] ={};
	double avgMY2[(int)N_temps] ={};
	double avgMX4[(int)N_temps] ={};
	double avgMY4[(int)N_temps] ={};
	double avgMXY2[(int)N_temps] ={};

	double avgMX2E[(int)N_temps] ={};
	double avgMY2E[(int)N_temps] ={};
	double avgMX4E[(int)N_temps] ={};
	double avgMY4E[(int)N_temps] ={};
	double avgMXY2E[(int)N_temps] ={};

	double avgExpFac[(int)N_temps] = {};
	double expFac;

	for ( int i = 0; i < Nsamples; ++i){
		//make a cluster
		newCluster(lattice,cluster,L,beta,randgen,TotXMag,TotYMag,TotEn);
		//take sample data
		for (int i = 0; i<N_temps; ++i){
			expFac = exp(-( (1/(extT[i])) - beta)*TotEn);
			avgExpFac[i] += expFac;
			avgE[i] += expFac*TotEn;
			avgE2[i] += expFac*TotEn*TotEn;
			avgM[i] += expFac*sqrt(TotXMag*TotXMag + TotYMag*TotYMag);
			avgMX2[i] += expFac*TotXMag*TotXMag;
			avgMY2[i] += expFac*TotYMag*TotYMag;
			avgMX4[i] += expFac*TotXMag*TotXMag*TotXMag*TotXMag;
			avgMY4[i] += expFac*TotYMag*TotYMag*TotYMag*TotYMag;
			avgMXY2[i] += expFac*TotXMag*TotXMag*TotYMag*TotYMag;
			avgMX2E[i] += expFac*TotXMag*TotXMag*TotEn;
			avgMY2E[i] += expFac*TotYMag*TotYMag*TotEn;
			avgMX4E[i] += expFac*TotXMag*TotXMag*TotXMag*TotXMag*TotEn;
			avgMY4E[i] += expFac*TotYMag*TotYMag*TotYMag*TotYMag*TotEn;
			avgMXY2E[i] += expFac*TotXMag*TotXMag*TotYMag*TotYMag*TotEn;
		}

	}
	//test if avgM4 is correct
	// conclusion: it wasnt
	/*
	   double testM4 = 0;
	   for (int i = 0; i< N_temps; ++i){
	   testM4 = avgMX4[i] + avgMX4[i] + 2*avgMXY2[i];
	   testM4 /= Nsamples;
	   cout << testM4 << "test:avgM4 " << avgM4[i]/Nsamples << endl;
	   }
	   */



	//calculate quantities of interest
	//derived quantites
	double xi[(int)N_temps] = {};//susceptibility
	double b[(int)N_temps] = {}; //Binder parameter
	double dbdt[(int)N_temps] = {};//derivative wrt T of Binder parameter
	for (int i =0; i< N_temps; ++i){
		//form averages of <M^2>, <M^4>, <M^2 E> and <M^4 E>
		avgM2[i] = avgMX2[i] + avgMY2[i];
		avgM4[i] = avgMX4[i] + avgMY4[i] + 2*avgMXY2[i];
		avgM2E[i] = avgMX2E[i] + avgMY2E[i];
		avgM4E[i] = avgMX4E[i] + avgMY4E[i] + 2*avgMXY2E[i];

		//normalize
		avgExpFac[i] /= Nsamples;

		avgE[i] /= Nsamples;
		avgE2[i] /= Nsamples;
		avgM[i] /= Nsamples;
		avgM2[i] /= Nsamples;
		avgM4[i] /= Nsamples;
		avgM2E[i] /= Nsamples;
		avgM4E[i] /= Nsamples;

		avgE[i] /= avgExpFac[i];
		avgE2[i] /= avgExpFac[i];
		avgM[i] /= avgExpFac[i];
		avgM2[i] /= avgExpFac[i];
		avgM4[i] /= avgExpFac[i];
		avgM2E[i] /= avgExpFac[i];
		avgM4E[i] /= avgExpFac[i];
		//calculate
		b[i] = avgM4[i];
		b[i] /= (avgM2[i]*avgM2[i]);
		dbdt[i] = (avgM4E[i]/(avgM2[i]*avgM2[i]) + 2*avgM4[i]*avgE[i]/(avgM2[i]*avgM2[i]) - 3*avgM4[i]*avgM2E[i]/(avgM2[i]*avgM2[i]*avgM2[i]));
		dbdt[i] /= (extT[i])*(extT[i]);
		xi[i] = avgM2[i] - avgM[i]*avgM[i];
		xi[i] /= L*L*L*(extT[i]);
	}
	for (int i = 0;i< N_temps; ++i){
		cout << L << " ";
		cout << extT[i] << " ";
		cout << avgE[i]/(L*L*L) << " ";
		cout << avgM[i]/(L*L*L) << " ";
		cout << b[i] << " ";
		cout << dbdt[i] << " ";
		cout << xi[i] << " ";
		cout << N_equil_steps/(L*L*L) << " ";
		cout << endl;

	}
}
