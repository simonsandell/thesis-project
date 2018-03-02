#include <iostream>
#include <random>
#include <functional>
#include <climits>
using namespace std;

double getP( auto &randgen){
	double p = randgen();
	return p;
}
int main() {
	uniform_real_distribution<double> dist(0,1);
	mt19937_64 eng; 
	int  j;
	cin >> j;
	eng.seed(j);
	auto gen = bind(dist,eng);

	double w = exp(-8);
	double p = gen();
	double avg = 0;
	for (int j = 0; j < 100; ++j){
	int i = 0;

	p = gen();
	while (w< p && i< INT_MAX){
		p = getP(gen);
		++i;
	}	
	avg += i;
	}
	cout <<  avg/100 << endl;
}
