#include <iostream>
#include <random>
#include <functional>

using namespace std;

//Randomization stuff

uniform_real_distribution<double> dist(0,1);
mt19937_64 eng; 
auto gen = bind(dist,eng);

int neighboursum(int **lat,int *a, int L){
	int sum =0;
		
	sum += lat[(a[0] + L +1)% L][a[1]];
	sum += lat[(a[0] + L -1)% L][a[1]];
	sum += lat[a[0]][(a[1] + L +1)% L];
	sum += lat[a[0]][(a[1] + L -1)% L];
	return sum;
}

void update(int **lattice,int L, double energydiffs[], double TotEnergy){
	//do one sweep
	for ( int i = 0; i < L*L; ++i)
	{
	//select random spin
	int s1 = gen()*(L-1);
	int s2 = gen()*(L-1);
	int s[2] = {s1,s2};
	//find neighbours
	int neighsum = neighboursum(lattice,s,L);
	//prob of transition
	double  w = energydiffs[8+neighsum];
	double p = gen();
	if (p < w){
		TotEnergy += neighsum;
		lattice[s1][s2] = -lattice[s1][s2];
	}
	}
}

int main(){
	
	//parameters and physical quantities
	unsigned int L = 4;
	double J = 1;
	double T = 1;
	double beta = 1/T;
	double TotEnergy = -2*L*L;
	//other intializations
	double energydiffs[17];
	for (int dE = -8; dE<9; ++dE){
		energydiffs[8+dE] = exp(-J*beta*dE);
	}
	//initialize lattice with all spins up
	int ** lattice;
	lattice = new int*[L];
	for (int i = 0; i< L;++i){
		lattice[i] = new int[L];
	}
	for (int i = 0; i<L;++i){
		for (int j=0; j<L;++j){
			lattice[i][j] = 1;
		}
	}
	//start simulation
	//discard first 10^3 sweeps 
	int discards = 10^3;	
	for (int i =0; i<discards; ++i){
		update(lattice, L, energydiffs,TotEnergy);
	}
	
	//hopefully we have equilibrated now
	//Calculate Stuff of interest
	//Only collect data once every 2 sweeps.
	double avgEn = 0;
	double avgEn2 = 0;
	int Nsamples = 1000;
	for (int i = 0; i < Nsamples; ++i){
	//2 sweeps, then collect data	
		update(lattice,L,energydiffs,TotEnergy);
		update(lattice,L,energydiffs,TotEnergy);
		avgEn += TotEnergy;
		avgEn2 += TotEnergy*TotEnergy;
	}
	avgEn /= Nsamples;
	avgEn2 /= Nsamples;

	double c = (avgEn2 - avgEn)/T/L/L;
	cout << c << endl;
	cout << TotEnergy << endl;

	cout << avgEn << endl;
	for(int i =0; i<L;++i){
		for(int j=0;j<L; ++j){
			cout<< lattice[i][j];
		}
		cout<<endl;
	}
}

