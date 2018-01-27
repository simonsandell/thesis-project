//This program performs montecarlo simulation with the Wolff algorithm on the 2D Ising model 
//taking the system size L as input and outputting the
#include <iostream>
#include <cmath>
#include <random>
#include <functional>
#include <unistd.h>
#include <sys/syscall.h>
#include <linux/random.h>
#include <utility>

using namespace std;

void printLattice(int**lattice,double &L){
	cout << endl;
	for(int i = 0; i < L; ++i){
		for(int j = 0; j < L; ++j){
			cout << lattice[i][j];
		}
		cout << endl;
	}
	cout << endl;
}

//clear the cluster
void emptyCluster(int **cluster,double &L){
	for (int i = 0; i< L; ++i){
		for (int j = 0; j< L; ++j){
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

//calculate energy and magnetization of the lattice
void updateEnMag(int**lattice,double &L,double &TotMag,double &TotEnergy){
	double newEn = calcEn(lattice,L);
	double newMag = calcMag(lattice,L);
	TotMag = newMag;
	TotEnergy = newEn;
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
		
		++time;
		//check if it has the opposite spin as starting spin (since we already flipped it)
		if (lattice[s1][s2] == -lattice[current.first][current.second]){
			//time should increase for every tried bond
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

//generate starting spin
//start new cluster at that spin
//empty the clusterlattice when done
//return number of flipped spins
int newCluster(int** lattice, int**cluster,double &L,double &prob,auto &randgen){
	//select starting spin randomly
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

	//parameters and physical quantities
	//averages
	double avgE; //energy
	double avgE2;//squared energy
	double avgM; //abs of magnetization
	double avgM2;//squared magnetization
	double avgM4;//fourth power of magnetization
	double avgM2E;// squared magnetization times energy
	double avgM4E; // 4th power magnetization times energy

	//derived quantites
	double c;//heat capacity
	double xi;//susceptibility
	double b; //binding param
	double dbdt;//derivative wrt T of binding param


	//set system size and temperature from input arguments
	if (argc != 3 ){

		cout << "Usage: ./a.out <L> <T>" << endl;
		return -1;
	}
	double L = stod(argv[1]);
	double T = stod(argv[2]); 

	double TotEnergy;
	double TotMag;

	//this should be replaced by list of precalculated values depending on systemsize
	double N_equil_steps= 1000*L*L;
	double Nsamples = 1000*L*L; 

	//we only need one probability in the Wolff algorithm
	double prob = 1.0 - exp(-2/T);

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
	//equilibration for fixed amount of clusters instead
	/*
	for (int i =0; i< 10000; ++i){
		newCluster(lattice,cluster,L,prob,randgen);
	}
	*/

	//start collecting data
	avgE = 0;
	avgE2 = 0;
	avgM = 0;
	avgM2 = 0;
	avgM4 = 0;
	avgM2E = 0;
	avgM4E = 0;

	for ( int i = 0; i < Nsamples; ++i){
		//make a new cluster
		newCluster(lattice,cluster,L,prob,randgen);
		//update energy and magnetization
		updateEnMag(lattice,L,TotMag,TotEnergy);
		//take sample data
		avgE += TotEnergy;
		avgE2 += TotEnergy*TotEnergy;
		avgM += abs(TotMag);
		avgM2 += TotMag*TotMag;
		avgM4 += TotMag*TotMag*TotMag*TotMag;
		avgM2E += TotMag*TotMag*TotEnergy;
		avgM4E += TotMag*TotMag*TotMag*TotMag*TotEnergy;
	}

	//normalize
	avgE /= Nsamples;
	avgE2 /= Nsamples;
	avgM /= Nsamples;
	avgM2 /= Nsamples;
	avgM4 /= Nsamples;
	avgM2E /= Nsamples;
	avgM4E /= Nsamples;

	//calculate quantities of interest
	c = avgE2 - avgE*avgE;
	c /= L*L*T*T;
	b = avgM4/(avgM2*avgM2);
	dbdt = (avgM4E/(avgM2*avgM2) + 2*avgM4*avgE/(avgM2*avgM2) - 3*avgM4*avgM2E/(avgM2*avgM2*avgM2));
	dbdt /= T*T;
	xi = avgM2 - avgM*avgM;
	xi /= L*L*T;

	cout << b << " " << dbdt << " " << xi;
}
