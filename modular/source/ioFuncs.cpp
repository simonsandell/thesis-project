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
void printOutput(long double L, long double T, long double Neqsw, long double Neqcl,long double Nsmsw,long double Nsmcl, long double cold, long double E, long double E2, long double M, long double M2, long double M4, long double M2E, long double M4E, long double SX2, long double SY2, long double SZ2, long double bin, long double dbdt, long double xi, long double rs, long double expFac){
	typedef std::numeric_limits<long double> dbl;

	std::cout.precision(dbl::max_digits10 + 5);

	std::cout << std::fixed << L << " ";				//0
	std::cout << std::fixed << T << " ";				//1
	std::cout << std::fixed << Neqsw << " ";				//1
	std::cout << std::fixed << Neqcl << " ";				//1
	std::cout << std::fixed << Nsmsw << " ";				//1
	std::cout << std::fixed << Nsmcl << " ";				//1
	std::cout << std::fixed << cold << " ";				//1
	std::cout << std::fixed << E << " ";				//2
	std::cout << std::fixed << E2 << " ";				//2
	std::cout << std::fixed << M << " ";				//3
	std::cout << std::fixed << M2 << " ";				//3
	std::cout << std::fixed << M4 << " ";				//3
	std::cout << std::fixed << M2E << " ";				//3
	std::cout << std::fixed << M4E << " ";				//3
	std::cout << std::fixed << SX2 << " ";				//3
	std::cout << std::fixed << SY2 << " ";				//3
	std::cout << std::fixed << SZ2 << " ";				//3
	std::cout << std::fixed << bin << " ";				//4
	std::cout << std::fixed << dbdt << " ";				//5
	std::cout << std::fixed << xi << " ";				//6
	std::cout << std::fixed << rs << " ";				//7
	std::cout << std::fixed << expFac << " ";				//7
	std::cout << std::endl;				
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

