#include <string>
#include <sstream>
#include <limits>
#include <ctime>
#include <iostream>
#include <fstream>
#include <unistd.h>
#include <limits.h>

#include "Ising3Dio.h"
#include "Ising3Dlattice.h"
#include "../avgStruct.h"

//print lattice
void printLatticeIsing3D(long double ***lattice,long double  L){
	typedef std::numeric_limits<long double> dbl;
	std::cout.precision(dbl::max_digits10 + 5);
	for(int i = 0; i < L; ++i){
		for(int j = 0; j < L; ++j){
			for(int k =0; k<L; ++k){
				std::cout << lattice[i][j][k] << " ";
			}
			std::cout << std::endl;
		}
		std::cout << std::endl;
	}
}
std::string get_selfpath2(){
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
void printIsing3DOutput(LatticeIsing3D lat, long double T,avgStruct avgs, long double bin, long double dbdt, long double xi, long double c){
	typedef std::numeric_limits<long double> dbl;

	std::cout.precision(dbl::max_digits10 + 5);
	std::stringstream sstrm;
	sstrm.precision(dbl::max_digits10 + 5);

	sstrm << std::fixed << lat.L << " ";				// L	0
	sstrm << std::fixed << T << " ";				// T	1
	sstrm << std::fixed << lat.Neqsweeps << " ";			// n	2
	sstrm << std::fixed << lat.Neqclusts << " ";			// n	3
	sstrm << std::fixed << lat.NTotSweeps<< " ";			// n	4
	sstrm << std::fixed << lat.NTotClusts<< " ";			// n	5
	sstrm << std::fixed << lat.coldstart << " ";			// cold	6
	sstrm << std::fixed << avgs.e	<< " ";				// e	7
	sstrm << std::fixed << avgs.e2	<< " ";				// e2	8
	sstrm << std::fixed << avgs.m	<< " ";				// m	9
	sstrm << std::fixed << avgs.m2	<< " ";				// m2	10
	sstrm << std::fixed << avgs.m4	<< " ";				// m4	11
	sstrm << std::fixed << avgs.m2e	<< " ";				// m2e	12
	sstrm << std::fixed << avgs.m4e	<< " ";				// m4e	13
	sstrm << std::fixed << bin	<< " ";				// b	14
	sstrm << std::fixed << dbdt	<< " ";				// dbdt	15
	sstrm << std::fixed << xi	<< " ";				// xi	16
	sstrm << std::fixed << c	<< " ";				// c	17
	sstrm << std::fixed << avgs.exp << " ";				// exp 	18 
	sstrm << std::endl;				
	std::cout << sstrm.str();
}

long double getMaxEIsing3D(long double L){
	std::ostringstream mstream;
	std::string exePath = get_selfpath2();
	mstream << exePath << "/maxE/Ising3D/" << L << "_maxE.txt";
	std::string fname = mstream.str();
	std::ifstream file(fname);
	long double maxE;
	file >> std::fixed >> maxE;
	return maxE;
}
void setMaxEIsing3D(long double L,long double newE){

	time_t  t = time(0);
	struct tm * now = localtime(& t);

	char buffer [80];
	strftime (buffer,80,"%Y-%m-%d.%H:%M:%S",now);
	std::ostringstream mstream;
	std::string exePath = get_selfpath2();
	mstream << exePath<< "/maxE/Ising3D/" << L <<"_"<< buffer;
	std::string fname = mstream.str();
	std::ofstream file;
	file.open(fname);

	typedef std::numeric_limits<long double> dbl;
	file.precision(dbl::max_digits10 +2);
	file << std::fixed << newE;
}

void saveLatticeIsing3D(LatticeIsing3D lat){

	int L = lat.L;
	std::ostringstream mstream;
	std::string exePath = get_selfpath2();
	mstream << exePath<< "/warmLattice/" << L <<"_warm.lat";
	std::string fname = mstream.str();
	FILE* output;
	output = std::fopen(fname.c_str(),"wb");
	fwrite(&lat,sizeof(lat),1,output);
	fclose(output);

}

LatticeIsing3D getLattice(int l){
	std::ostringstream mstream;
	std::string exePath = get_selfpath2();
	mstream << exePath << "/warmLattice/" << l << "_warm.lat";
	std::string fname = mstream.str();

	LatticeIsing3D lat;
	FILE* input;

	input = fopen(fname.c_str(),"rb");

	size_t result= fread(&lat,sizeof(lat),1,input);
	if (result != 1){
		std::cout << "failed to load lattice" << std::endl;
		exit(1);
	}

	fclose(input);

	return lat;
}

