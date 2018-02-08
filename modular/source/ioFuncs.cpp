#include <string>
#include <sstream>
#include <limits>
#include <ctime>
#include <iostream>
#include <fstream>
#include "ioFuncs.h"

void printOutput(long double L,long double T, long double E, long double M, long double bin, long double dbdt,long double xi,long double rs, long double N_eq_sweeps, int N_eq_clusts,bool cold){

	std::cout << std::fixed << L << " ";
	std::cout << std::fixed << T << " ";
	std::cout << std::fixed << E << " ";
	std::cout << std::fixed << M << " ";
	std::cout << std::fixed << bin << " ";
	std::cout << std::fixed << dbdt << " ";
	std::cout << std::fixed << xi << " ";
	std::cout << std::fixed << rs << " ";
	std::cout << std::fixed << N_eq_sweeps << " "; 
	std::cout << std::fixed << N_eq_clusts << " "; 
	std::cout << cold << " "; 
	std::cout << std::fixed << std::endl;
}

long double getMaxE(long double L){
	std::ostringstream mstream;
	mstream << "/home/simsan/exjobb/modular/maxE/" << L << "_maxE.txt";
	std::string fname = mstream.str();
	std::ifstream file(fname);
	long double maxE;
	file >> std::fixed >> maxE;
	return maxE;
}
void setMaxE(long double L,long double newE){

	time_t  t = time(0);
	struct tm * now = localtime(& t);

	char buffer [80];
	strftime (buffer,80,"%Y-%m-%d.%H:%M:%S",now);
	std::ostringstream mstream;
	mstream << "/home/simsan/exjobb/modular/maxE/" << L <<"_"<< buffer;
	std::string fname = mstream.str();
	std::ofstream file;
	file.open(fname);

	typedef std::numeric_limits<long double> dbl;
	file.precision(dbl::max_digits10 +2);
	file << std::fixed << newE;
}
