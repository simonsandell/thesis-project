//This program performs the montecarlo with the Wolff algorithm simulation of the 2D Ising model at the critical temperature
//taking the system size L as input and outputting binder parameter, db/dt and xi
//
//Implements histogramextrapolation to obtain values at different temperatures
#include <iostream>
#include <cmath>
#include <random>
#include <functional>
#include <unistd.h>
#include <sys/syscall.h>
#include <linux/random.h>
#include <iomanip>
#include <utility>

using namespace std;
//empty the cluster
void emptyCluster(int **cluster, double&L){
	for(int i = 0; i<L; ++i){
		for(int j = 0; j<L; ++j){
			cluster[i][j] = 0;
		}
	}
}
//sum of nearest neighbours 
double nnSum(int** lattice,double &L, int &s1, int &s2){
	//find indices
	int n1m = (s1 -1 + (int)L )%(int)L;
	int n1p = (s1 +1 + (int)L )%(int)L;
	int n2m = (s2 -1 + (int)L )%(int)L;
	int n2p = (s2 +1 + (int)L )%(int)L;
	return lattice[s1][n2m] + lattice[s1][n2p] + lattice[n1m][s2] + lattice[n1p][s2];
}
//calc Energy
double calcEn(int** lattice, double&L){
	double ret = 0;
	for ( int i = 0; i<L; ++i){
		for ( int j = 0; j<L; ++j){
			ret += -lattice[i][j]*nnSum(lattice,L,i,j);
		}
	}
	//avoid doublecounting
	ret = 0.5*ret;
	return ret;
}
//calc magnetization
double calcMag(int** lattice, double&L){
	double ret = 0;
	for ( int i = 0; i<L; ++i){
		for ( int j = 0; j<L; ++j){
			ret += lattice[i][j];
		}
	}
	return abs(ret);
}
void updateEnMag(int **lattice,double &L, double &TotMag,double &TotEn){
	double newMag = calcMag(lattice,L);
	double newEn = calcEn(lattice,L);
	TotMag = newMag;
	TotEn = newEn;
}

//make a cluster..
int growCluster(int s1,int s2,int **lattice,int **cluster, double &L, double &prob, auto &randgen){

	int time = 1;
	//flip spin and mark as part of cluster
	lattice[s1][s2] = -lattice[s1][s2];
	cluster[s1][s2] = 1;

	//find indices of nearest neighbours
	int n1m = (s1 -1 + (int)L )%(int)L;
	int n1p = (s1 +1 + (int)L )%(int)L;
	int n2m = (s2 -1 + (int)L )%(int)L;
	int n2p = (s2 +1 + (int)L )%(int)L;
	//add them to perimeter list if they are equal spin as first
	pair<int,int> perimeter[(int)(L*L*4)] = {};
	//index at which we want to add another perimeter spin
	//so if it is equal to 0, it means the list is empty
	//consequently the index of the last spin is n-1
	int n = 0;
	if (lattice[s1][s2] == -lattice[n1m][s2]){perimeter[n] = make_pair(n1m,s2); n +=1;}
	if (lattice[s1][s2] == -lattice[n1p][s2]){perimeter[n] = make_pair(n1p,s2); n +=1;}
	if (lattice[s1][s2] == -lattice[s1][n2m]){perimeter[n] = make_pair(s1,n2m); n +=1;}
	if (lattice[s1][s2] == -lattice[s1][n2p]){perimeter[n] = make_pair(s1,n2p); n +=1;}
	pair<int,int> current;
	while (n > 0){
		//pick out the last element 
		current = perimeter[n-1];
		n -= 1;
		
		//check if it has the opposite spin as starting spin (since we already flipped it)
		if (lattice[s1][s2] == -lattice[current.first][current.second]){
			//time should increase for every tried bond
			++time;
			//add this perimeter spin to the cluster with probability prob
			if (randgen() < prob){
				//flip spin and mark it as added to the cluster
				lattice[current.first][current.second] = -lattice[current.first][current.second];
				cluster[current.first][current.second] = 1;
				//find indices of its neighbours
				pair<int,int> neig1 = make_pair((current.first + 1) % (int)L, current.second);
				pair<int,int> neig2 = make_pair(((int)L + current.first - 1) % (int)L, current.second);
				pair<int,int> neig3 = make_pair(current.first, (current.second + 1) % (int)L);
				pair<int,int> neig4 = make_pair(current.first, (current.second + (int)L - 1) % (int)L);
				//if it is not already part of the cluster, add it to perimeter list
				if (cluster[neig1.first][neig1.second] ==0){
					perimeter[n] = neig1;
					n = n + 1;
				}
				if (cluster[neig2.first][neig2.second] ==0){
					perimeter[n] = neig2;
					n = n + 1;
				}
				if (cluster[neig3.first][neig3.second] ==0){
					perimeter[n] = neig3;
					n = n + 1;
				}
				if (cluster[neig4.first][neig4.second] ==0){
					perimeter[n] = neig4;
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
int newCluster(int** lattice, int**cluster,double &L,double &prob,auto &randgen){
	int s1 = L*randgen();
	int s2 = L*randgen();
	int time;
	time = growCluster(s1,s2,lattice,cluster,L,prob,randgen);
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
	if (argc != 2 ){

		cout << "Usage: ./a.out <L>" << endl;
		return -1;
	}
	double L = stod(argv[1]);
	//critical temperature of 2dIsing
	double T = 2.26918531421;

	double beta = 1/T;
	double TotEn;
	double TotMag;

	//
	//Set equilibration time and number of samples
	double N_equil_steps= 100*L*L;
	double Nsamples = 10000; 

	//we only need one probability in the Wolff algorithm
	double prob = 1 - exp(-2*beta);

	//define and initialize the lattice and cluster
	int **lattice;
	int **cluster;
	lattice = new int*[(int)L];
	cluster = new int*[(int)L];
	for (int i = 0; i< L;++i){
		lattice[i] = new int[(int)L];
		cluster[i] = new int[(int)L];
	}
	for (int i = 0; i<L;++i){
		for (int j=0; j<L;++j){
			lattice[i][j] = 1;
			cluster[i][j] = 0;
		}
	}

	//eqilibration 
	int t = 0;
	while (t < N_equil_steps){
		t += newCluster(lattice,cluster,L,prob,randgen);
	}

	//start collecting data
	
	//histogram extrapolation
	int N_temps = 22;
	double extT[N_temps] = {2.10,2.12,2.14,2.16,2.18,2.20,2.22,2.24,2.26,2.26918531421,2.28,2.30,2.32,2.34,2.36,2.38,2.40,2.42,2.44,2.46,2.48,2.50};

	//parameters and physical quantities
	//averages
	double avgE[N_temps] = {}; //energy
	double avgE2[N_temps] = {};//squared energy
	double avgM[N_temps] = {}; //abs of magnetization
	double avgM2[N_temps] = {};//squared magnetization
	double avgM4[N_temps] = {};//fourth power of magnetization
	double avgM2E[N_temps] = {};// squared magnetization times energy
	double avgM4E[N_temps] = {}; // 4th power magnetization times energy
	
	double avgExpFac[N_temps] = {};

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
	double xi[N_temps] = {};//susceptibility
	double b[N_temps] = {}; //Binder parameter
	double dbdt[N_temps] = {};//derivative wrt T of Binder parameter
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
		xi[i] /= L*L*(extT[i]);
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
