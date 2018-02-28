//This program performs the montecarlo with the Wolff algorithm simulation of the 2D Ising model
// FOR EQUILIBRATION TIME STUDY
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

void printLattice(int**lattice,double &L){
	for(int i = 0; i < L; ++i){
		for(int j = 0; j < L; ++j){
			cout << lattice[i][j];
		}
		cout << endl;
	}
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
		
		//check if it has the opposite spin as starting spin (since we already flipped it)
		//necessary since a spin may be added twice to the perimeter list
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
	int steps;
	steps = growCluster(s1,s2,lattice,cluster,L,prob,randgen);
	emptyCluster(cluster,L);
	return steps;
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
	double avgM; //abs of magnetization


	//set system size and temperature from input arguments
	if (argc != 5 ){
		cout << "Usage: ./a.out <L> <T> <N_sweeps> <startM>" << endl;
		return -1;
	}
	double L = stod(argv[1]);
	double T = stod(argv[2]);
	double N_eq_sweeps = stod(argv[3]);
	int startM = atoi(argv[4]);


	double beta = 1/T;
	double TotEnergy;
	double TotMag;

	//we only need one probability in the Wolff algorithm
	double prob = 1 - exp(-2*beta);

	//define and initialize the lattice with all spins up
	int **lattice;
	int **cluster;
	lattice = new int*[(int)L];
	cluster = new int*[(int)L];
	for (int i = 0; i< L;++i){
		lattice[i] = new int[(int)L];
		cluster[i] = new int[(int)L];
	}
	if (startM == 1){
		for (int i = 0; i<L;++i){
			for (int j=0; j<L;++j){
				lattice[i][j] = 1;
				cluster[i][j] = 0;
			}
		}
	}
	if (startM == 0){
		int k = 1;
		for (int i = 0; i<L;++i){
			for (int j=0; j<L;++j){
				lattice[i][j] = k;
				k = -k;
				cluster[i][j] = 0;
			}
		}
	}

	//eqilibration 
	int steps = 0;
	while (steps < N_eq_sweeps*L*L){
		steps += newCluster(lattice,cluster,L,prob,randgen);
	}

	updateEnMag(lattice,L,TotMag,TotEnergy);

	double time = steps/(L*L);

	cout << time << " " << abs(TotMag) << endl;


}
