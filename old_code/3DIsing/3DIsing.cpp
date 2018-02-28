//This program performs montecarlo with the Wolff algorithm simulation of the 3D Ising model at the critical temperature
//Tc = 4.515;
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

void printLattice(int***lattice,double &L){
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
void emptyCluster(int ***cluster,double &L){
	int steps = 0;
	for (int i = 0; i< L; ++i){
		for (int j = 0; j< L; ++j){
			for (int k = 0; k<L; ++k){	
				cluster[i][j][k] = 0;
			}
		}
	}
}

//sum of nearest neighbours 
double nnSum(int*** lattice,double &L, int &s1, int &s2, int &s3){
	double sum = 0;
	int n1m = (s1 -1 + (int)L )%(int)L;
	int n1p = (s1 +1 + (int)L )%(int)L;
	int n2m = (s2 -1 + (int)L )%(int)L;
	int n2p = (s2 +1 + (int)L )%(int)L;
	int n3m = (s3 -1 + (int)L )%(int)L;
	int n3p = (s3 +1 + (int)L )%(int)L;
	sum += lattice[n1m][s2][s3];
	sum += lattice[n1p][s2][s3];
	sum += lattice[s1][n2m][s3];
	sum += lattice[s1][n2p][s3];
	sum += lattice[s1][s2][n3m];
	sum += lattice[s1][s2][n3p];
	return sum;
}
double calcMag(int ***lattice,double&L){
	double mag = 0;
	for (int i = 0; i< L; ++i){
		for (int j = 0; j< L; ++j){
			for (int k = 0; k<L; ++k){	
				mag += lattice[i][j][k];	
			}
		}
	}
	return mag;
}	

double calcEn(int***lattice,double&L){

	double en = 0;
	for (int i = 0; i< L; ++i){
		for (int j = 0; j< L; ++j){
			for (int k = 0; k<L; ++k){	
				en+= -lattice[i][j][k]*nnSum(lattice,L,i,j,k);	
			}
		}
	}
	en = 0.5*en;
	return en;
}
//calculate energy and magnetization of the lattice
void updateEnMag(int***lattice,double &L,double &TotMag,double &TotEn){
	double newEn= calcEn(lattice,L);
	double newMag = abs(calcMag(lattice,L));
	TotEn = newEn;
	TotMag = newMag;
}

//make a cluster..
int growCluster(int s1,int s2,int s3,int ***lattice,int ***cluster, double &L, double &prob, auto &randgen){

	int time = 1;
	//flip spin and mark as part of cluster
	lattice[s1][s2][s3] = -lattice[s1][s2][s3];
	cluster[s1][s2][s3] = 1;

	//find indices of nearest neighbours
	int n1m = (s1 -1 + (int)L )%(int)L;
	int n1p = (s1 +1 + (int)L )%(int)L;
	int n2m = (s2 -1 + (int)L )%(int)L;
	int n2p = (s2 +1 + (int)L )%(int)L;
	int n3m = (s3 -1 + (int)L )%(int)L;
	int n3p = (s3 +1 + (int)L )%(int)L;
	//add them to perimeter list if they are equal spin as first
	tuple<int,int,int> perimeter[(int)(L*L*L*6)] = {};
	//index at which we want to add another perimeter spin
	//so if it is equal to 0, it means the list is empty
	//consequently the index of the last spin is n-1
	int n = 0;
	if (lattice[s1][s2][s3] == -lattice[n1m][s2][s3]){perimeter[n] = make_tuple(n1m,s2,s3); n +=1;}
	if (lattice[s1][s2][s3] == -lattice[n1p][s2][s3]){perimeter[n] = make_tuple(n1p,s2,s3); n +=1;}
	if (lattice[s1][s2][s3] == -lattice[s1][n2m][s3]){perimeter[n] = make_tuple(s1,n2m,s3); n +=1;}
	if (lattice[s1][s2][s3] == -lattice[s1][n2p][s3]){perimeter[n] = make_tuple(s1,n2p,s3); n +=1;}
	if (lattice[s1][s2][s3] == -lattice[s1][s2][n3m]){perimeter[n] = make_tuple(s1,s2,n3m); n +=1;}
	if (lattice[s1][s2][s3] == -lattice[s1][s2][n3p]){perimeter[n] = make_tuple(s1,s2,n3p); n +=1;}
	tuple<int,int,int> current;
	while (n > 0){
		//pick out the last element 
		current = perimeter[n-1];
		n -= 1;

		//check if it has the opposite spin as starting spin (since we already flipped it)
		if (lattice[s1][s2][s3] == -lattice[get<0>(current)][get<1>(current)][get<2>(current)]){
			//time should increase for every tried bond
			++time;
			//add this perimeter spin to the cluster with probability prob
			if (randgen() < prob){
				//flip spin and mark it as added to the cluster
				lattice[get<0>(current)][get<1>(current)][get<2>(current)] = -lattice[get<0>(current)][get<1>(current)][get<2>(current)];
				cluster[get<0>(current)][get<1>(current)][get<2>(current)] = 1;
				//find indices of its neighbours
				tuple<int,int,int> neig1 = make_tuple((get<0>(current) + 1) % (int)L, get<1>(current),get<2>(current));
				tuple<int,int,int> neig2 = make_tuple(((int)L + get<0>(current) - 1) % (int)L, get<1>(current),get<2>(current));
				tuple<int,int,int> neig3 = make_tuple(get<0>(current), (get<1>(current) + 1) % (int)L,get<2>(current));
				tuple<int,int,int> neig4 = make_tuple(get<0>(current), (get<1>(current) + (int)L - 1) % (int)L,get<2>(current));
				tuple<int,int,int> neig5 = make_tuple(get<0>(current), get<1>(current), (1 + get<2>(current))%(int)L);
				tuple<int,int,int> neig6 = make_tuple(get<0>(current), get<1>(current), (get<2>(current)+(int)L -1 )%(int)L);
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
//generate starting spin
//empty the cluster when done
//return number of flipped spins
int newCluster(int*** lattice, int***cluster,double &L,double &prob,auto &randgen){
	int s1 = L*randgen();
	int s2 = L*randgen();
	int s3 = L*randgen();
	int time;
	time = growCluster(s1,s2,s3,lattice,cluster,L,prob,randgen);
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
	double L = stod(argv[1]);
	double extT[argc -2];
	double N_temps = argc -2;
	for (int i = 0; i< (argc-2); ++i){
		extT[i] = stod(argv[i+2]);
	}		
	//critical temperature of 3D XY
	double T = 4.515; 
	double beta = 1/T;

	double TotEn;
	double TotMag;

	//
	//Set equilibration time and number of samples
	double N_equil_steps= 100*L*L*L;
	double Nsamples = 10000; 

	//we only need one probability in the Wolff algorithm
	double prob = 1 - exp(-2*beta);

	//define and initialize the lattice and cluster
	int ***lattice;
	int ***cluster;
	lattice = new int**[(int)L];
	cluster = new int**[(int)L];
	for (int i = 0; i< L;++i){
		lattice[i] = new int*[(int)L];
		cluster[i] = new int*[(int)L];
		for (int j =0;j<L;++j){
			lattice[i][j] = new int[(int)L];
			cluster[i][j] = new int[(int)L];
		}
	}
	for (int i = 0; i<L;++i){
		for (int j=0; j<L;++j){
			for (int k = 0; k<L; ++k){
				lattice[i][j][k] = 1;
				cluster[i][j][k] = 0;
			}
		}
	}

	//eqilibration 
	int t = 0;
	while (t < N_equil_steps){
		t += newCluster(lattice,cluster,L,prob,randgen);
	}

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

	double avgExpFac[(int)N_temps] = {};

	double expFac;


	for ( int i = 0; i < Nsamples; ++i){
		//make a cluster
		newCluster(lattice,cluster,L,prob,randgen);
		//update energy and magnetization
		updateEnMag(lattice,L,TotMag,TotEn);
		//take sample data
		for (int i = 0; i<N_temps; ++i){
			expFac = exp(-( (1/(extT[i])) - beta)*TotEn);
			avgExpFac[i] += expFac;
			avgE[i] += (expFac)*TotEn;
			avgE2[i] += (expFac)*TotEn*TotEn;
			avgM[i] += (expFac)*abs(TotMag);
			avgM2[i] += (expFac)*TotMag*TotMag;
			avgM4[i] += (expFac)*TotMag*TotMag*TotMag*TotMag;
			avgM2E[i] += (expFac)*TotMag*TotMag*TotEn;
			avgM4E[i] += (expFac)*TotMag*TotMag*TotMag*TotMag*TotEn;
		}

	}

	//calculate quantities of interest
	//derived quantites
	double xi[(int)N_temps] = {};//susceptibility
	double b[(int)N_temps] = {}; //Binder parameter
	double dbdt[(int)N_temps] = {};//derivative wrt T of Binder parameter
	for (int i =0; i< N_temps; ++i){
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
	for (int i = 0;i<N_temps;++i){
		cout << b[i] << " ";
	}
	for (int i = 0;i<N_temps;++i){
		cout << dbdt[i] << " ";
	}
	for (int i = 0;i<N_temps;++i){
		cout << xi[i] << " ";
	}
}
