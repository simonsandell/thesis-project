#include <string>
#include <sstream>
#include <limits>
#include <ctime>
#include <iostream>
#include <fstream>
#include <unistd.h>
#include <limits.h>

#include "ioFuncs.h"

std::string get_selfpath(){
	char buff[PATH_MAX];
	ssize_t len = ::readlink("/proc/self/exe",buff,sizeof(buff)-1);
	if (len != -1) {
		buff[len] = '\0';
		std::string strbuff = std::string(buff);
		const size_t lastslash = strbuff.rfind('/');
		strbuff = strbuff.substr(0,lastslash);
		return strbuff;
	}
	else {
		std::cout << "selfpath fail" << std::endl;
		exit(-1);
	}
}

void printOutput(long double L,long double T, long double E, long double M, long double bin, long double dbdt,long double xi,long double rs, long double N_eq_sweeps, int N_eq_clusts,bool cold){
	typedef std::numeric_limits<long double> dbl;

	std::cout.precision(dbl::max_digits10 + 5);

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
	std::string exePath = get_selfpath();
	mstream << exePath << "/maxE/" << L << "_maxE.txt";
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
	std::string exePath = get_selfpath();
	mstream << exePath<< "/maxE/" << L <<"_"<< buffer;
	std::string fname = mstream.str();
	std::ofstream file;
	file.open(fname);

	typedef std::numeric_limits<long double> dbl;
	file.precision(dbl::max_digits10 +2);
	file << std::fixed << newE;
}

void saveLattice(long double L,long double Neqsw,long double Neqcl, long double***lattice){

	std::ostringstream mstream;
	std::string exePath = get_selfpath();
	mstream << exePath<< "/warmLattice/" << L <<"_warm.lat";
	std::string fname = mstream.str();
	std::ofstream file;
	file.open(fname);
	//first values saved is the number of equilibration sweeps and clusters
	file << Neqsw;
	file << " ";
	file << Neqcl;
	file << " ";

	typedef std::numeric_limits<long double> dbl;
	file.precision(dbl::max_digits10 +2);
	for (int p = 0; p<L; ++p){
		for (int q = 0; q<L; ++q){
			for (int r = 0; r<L; ++r){
				file << std::fixed << lattice[p][q][r];
				file << " ";
			}
		}
	}
}
long double *** getLattice(long double L,long double & Neqsw,long double& Neqcl){

	std::ostringstream mstream;
	std::string exePath = get_selfpath();
	mstream << exePath << "/warmLattice/" << L << "_warm.lat";
	std::string fname = mstream.str();
	std::ifstream file(fname);
	//first value saved is actually the # of equilibration sweeps.
	file >> Neqsw;
	file >> Neqcl;
	long double ***lattice;
	lattice = new long double **[(int)L];
	for (int i = 0; i< L;++i){
		lattice[i] = new long double *[(int)L];
		for (int j =0;j<L;++j){
			lattice[i][j] = new long double[(int)L];
			for (int k =0; k<L; ++k){
				file >> lattice[i][j][k];
			}
		}
	}
	return lattice;
}

