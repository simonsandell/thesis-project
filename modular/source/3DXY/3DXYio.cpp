#include <string>
#include <sstream>
#include <limits>
#include <ctime>
#include <iostream>
#include <fstream>
#include <unistd.h>
#include <limits.h>

#include "3DXYio.h"
#include "3DXYlattice.h"
#include "../avgStruct.h"
#include "../ioHandle.h"

//print lattice
void printLattice3DXY(long double ***lattice,long double  L){
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
void print3DXYOutput(Lattice3DXY &lat, long double T,avgStruct avgs, long double bin, long double dbdt, long double xi, long double rs){
	typedef std::numeric_limits<long double> dbl;

	std::cout.precision(dbl::max_digits10 + 5);
	std::stringstream sstrm;
	sstrm.precision(dbl::max_digits10 + 5);

	sstrm << std::fixed << lat.L << " ";				//0
	sstrm << std::fixed << T << " ";				//1
	sstrm << std::fixed << lat.Neqsweeps << " ";			//2
	sstrm << std::fixed << lat.Neqclusts << " ";			//3
	sstrm << std::fixed << lat.NTotSweeps << " ";			//4
	sstrm << std::fixed << lat.NTotClusts << " ";			//5
	sstrm << std::fixed << lat.coldstart << " ";			//6
	sstrm << std::fixed << avgs.e	<< " ";				//7
	sstrm << std::fixed << avgs.e2	<< " ";				//8
	sstrm << std::fixed << avgs.m	<< " ";				//9
	sstrm << std::fixed << avgs.m2	<< " ";				//10
	sstrm << std::fixed << avgs.m4	<< " ";				//11
	sstrm << std::fixed << avgs.m2e	<< " ";				//12
	sstrm << std::fixed << avgs.m4e	<< " ";				//13
	sstrm << std::fixed << avgs.s2x	<< " ";				//14
	sstrm << std::fixed << avgs.s2y	<< " ";				//15
	sstrm << std::fixed << avgs.s2z << " ";				//16
	sstrm << std::fixed << bin	<< " ";				//17
	sstrm << std::fixed << dbdt	<< " ";				//18
	sstrm << std::fixed << xi	<< " ";				//19
	sstrm << std::fixed << rs	<< " ";				//20
	sstrm << std::fixed << avgs.exp << " ";				//21
	sstrm << std::endl;				
	lat.oPer.addLine(sstrm.str());
}

long double getMaxE3DXY(long double L){
	std::ostringstream mstream;
	std::string exePath = get_selfpath();
	mstream << exePath << "/maxE/3DXY/" << L << "_maxE.txt";
	std::string fname = mstream.str();
	std::ifstream file(fname);
	long double maxE;
	file >> std::fixed >> maxE;
	return maxE;
}
void setMaxE3DXY(long double L,long double newE){

	time_t  t = time(0);
	struct tm * now = localtime(& t);

	char buffer [80];
	strftime (buffer,80,"%Y-%m-%d.%H:%M:%S",now);
	std::ostringstream mstream;
	std::string exePath = get_selfpath();
	mstream << exePath<< "/maxE/3DXY/" << L <<"_"<< buffer;
	std::string fname = mstream.str();
	std::ofstream file;
	file.open(fname);

	typedef std::numeric_limits<long double> dbl;
	file.precision(dbl::max_digits10 +2);
	file << std::fixed << newE;
}

void saveLattice3DXY(Lattice3DXY &lat){

	int L = lat.L;
	std::ostringstream mstream;
	std::string exePath = get_selfpath();
	mstream << exePath<< "/warmLattice/" << L <<"_warm.lat";
	std::string fname = mstream.str();
	FILE* output;
	output = std::fopen(fname.c_str(),"wb");
	fwrite(&lat,sizeof(lat),1,output);
	fclose(output);

}

Lattice3DXY getLattice3DXY(int l){
	std::ostringstream mstream;
	std::string exePath = get_selfpath();
	mstream << exePath << "/warmLattice/" << l << "_warm.lat";
	std::string fname = mstream.str();

	Lattice3DXY lat;
	FILE* input;

	input = fopen(fname.c_str(),"rb");


	size_t result = fread(&lat,sizeof(lat),1,input);
	if (result != 1){
		std::cout << "failed to load lattice" << std::endl;
		exit(1);
	}

	fclose(input);

	return lat;
}

