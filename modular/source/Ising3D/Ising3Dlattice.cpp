#include <iostream>
#include <sstream>
#include <string>
#include <fstream>
#include <unistd.h>
#include <random>
#include <cstring>
#include <cerrno>
#include <sys/syscall.h>

#include "Ising3Dlattice.h"
#include "Ising3Dio.h"
#include "../maxEHandle.h"

long double LatticeIsing3D::siteEnergy( int &s1, int &s2, int &s3){
	long double sum = 0.0L;
	//find indices of neighbours
	int n1m = (s1 -1 + int_L )%int_L;
	int n1p = (s1 +1 + int_L )%int_L;
	int n2m = (s2 -1 + int_L )%int_L;
	int n2p = (s2 +1 + int_L )%int_L;
	int n3m = (s3 -1 + int_L )%int_L;
	int n3p = (s3 +1 + int_L )%int_L;
	//sum 
	sum -= theLattice[s1][s2][s3]*theLattice[n1m][s2][s3];
	sum -= theLattice[s1][s2][s3]*theLattice[n1p][s2][s3];
	sum -= theLattice[s1][s2][s3]*theLattice[s1][n2m][s3];
	sum -= theLattice[s1][s2][s3]*theLattice[s1][n2p][s3];
	sum -= theLattice[s1][s2][s3]*theLattice[s1][s2][n3m];
	sum -= theLattice[s1][s2][s3]*theLattice[s1][s2][n3p];
	return sum;
}
//calculate sin(theta - theta_x) upwards +, downward -
long double LatticeIsing3D::calcMag(){
	long double ret = 0.0L;
	for (int i = 0; i<L; ++i){
		for (int j = 0; j<L; ++j){
			for (int k = 0; k<L; ++k){
				ret += theLattice[i][j][k];
			}
		}
	}
	return ret;
}

long double LatticeIsing3D::calcEn(){
	long double en = 0.0L;
	for (int i = 0; i< L; ++i){
		for (int j = 0; j< L; ++j){
			for (int k = 0; k<L; ++k){	
				en += siteEnergy(i,j,k);
			}
		}
	}
	en *= 0.5L;
	return en;
}

long double *** LatticeIsing3D::newLatticeI3D(long double L,bool cold){
	//make new lattice
	long double ***lattice;
	int intel = (int)( L + 0.5L);
	lattice = new long double **[intel];
	for (int i = 0; i< L;++i){
		lattice[i] = new long double *[intel];
		for (int j =0;j<L;++j){
			lattice[i][j] = new long double[intel];
		}
	}

	if (cold) {
		for (int i = 0; i<L;++i){
			for (int j=0; j<L;++j){
				for (int k = 0; k<L; ++k){
					lattice[i][j][k] = 1.0L;
				}
			}
		}
	}
	else {
		for (int i = 0; i<L;++i){
			for (int j=0; j<L;++j){
				for (int k = 0; k<L; ++k){
					if ( rand.rnd() >0.5L){
						lattice[i][j][k] =1.0L;
					}
					else {
						lattice[i][j][k] =-1.0L;
					}
				}
			}
		}
	}
	return lattice;
}
//update quantiites of the lattice
void LatticeIsing3D::updateQuants(){
	energy = calcEn();
	mag = calcMag();
};

//initialize new lattice
LatticeIsing3D::LatticeIsing3D(int l, bool cold,long double Beta,RandStruct r, Cluster c,std::string pathMaxE,std::string pathWarmLat)
	: rand(r), clust(c)
{
	beta = Beta;
	PROB = 1.0L - exp(-2.0L*beta);
	theLattice = newLatticeI3D((long double)l,cold);
	L = (long double)l;
	Nspins =L*L*L;
	Neqsweeps = 0.0L;
	Neqclusts = 0;
	NTotClusts = 0;
	int_L = (int)(L + 0.5L);
	NTotSweeps= 0.0L;
	coldstart = cold;
	warmedUp = false;

	warmLatPath = pathWarmLat;
	maxEPath = pathMaxE;
	maxE = getMaxE(pathMaxE,l);


	
	if (cold) {
		energy = -3.0L*Nspins;
		mag = Nspins;
	}
	else {
		energy = calcEn();
		mag = calcMag();
	}


};

LatticeIsing3D::LatticeIsing3D(){

}

void LatticeIsing3D::testConsistent(){

	typedef std::numeric_limits<long double> dbl;
	std::cout.precision(dbl::max_digits10 + 5);
	long double testEn = calcEn();
	long double testMag = calcMag();
	std::cout <<std::fixed<< energy - testEn << "  E    "<< energy << " "<< testEn << std::endl;
	std::cout <<std::fixed<< mag - testMag << "  M    "<< mag << " "<< testMag << std::endl;
}
std::string wlpathI3D(std::string wlp,long double l){
	time_t  t = time(0);
	struct tm * now = localtime(& t);

	char buffer [80];
	strftime (buffer,80,"%Y-%m-%d.%H:%M:%S",now);
	std::ostringstream mstream;
	mstream << wlp << l<<"_" << buffer  <<"_.lat";
	return mstream.str();
}
void LatticeIsing3D::saveLattice(){

	//save
	//	theLattice
	//	L,Neqsweeps,NTotSweeps,maxE,beta
	//	Neqclusts,NTotClusts
	//	coldstart,warmedUp
	//	warmLatPath,maxEPath
	
	if (oPer.outputLines.size() >0){
		std::cout << "loading failed, outPutter has lines" << std::endl;
		exit(1);
	}
	std::string fpath = wlpathI3D(warmLatPath,L);

	std::ofstream ofs(fpath.c_str(),std::ios::binary);
	if( ofs){
		//save theLattice
		for (int i = 0; i< L;++i){
			for (int j = 0; j< L;++j){
				for (int k = 0; k< L;++k){
					ofs.write(
					reinterpret_cast<char *>(&theLattice[i][j][k]),
					sizeof(theLattice[i][j][k])
					);
				}
			}
		}
		//save long doubles
		ofs.write(reinterpret_cast<char*>(& L) , sizeof( L ));
		ofs.write(reinterpret_cast<char*>(& Neqsweeps) , sizeof( Neqsweeps ));
		ofs.write(reinterpret_cast<char*>(& NTotSweeps) , sizeof( NTotSweeps ));
		ofs.write(reinterpret_cast<char*>(& maxE) , sizeof( maxE ));
		ofs.write(reinterpret_cast<char*>(& beta) , sizeof( beta));
		//save long ints
		ofs.write(reinterpret_cast<char*>(& Neqclusts) , sizeof( Neqclusts ));
		ofs.write(reinterpret_cast<char*>(& NTotClusts) , sizeof( NTotClusts ));
		//save bools
		ofs.write(reinterpret_cast<char*>(& coldstart) , sizeof( coldstart ));
		ofs.write(reinterpret_cast<char*>(& warmedUp) , sizeof( warmedUp ));
		//save strings
		size_t sz1 = warmLatPath.size();
		size_t sz2 = maxEPath.size();
		ofs.write(reinterpret_cast<char*>(&sz1),sizeof(sz1));
		ofs.write(warmLatPath.c_str() ,warmLatPath.size());
		ofs.write(reinterpret_cast<char*>(&sz2),sizeof(sz2));
		ofs.write(maxEPath.c_str() ,maxEPath.size());

		ofs.close();
	}
	else{
		std::cout << "file open failed" << std::endl;
		std::cout << std::strerror(errno) << std::endl;
	}
}

void LatticeIsing3D::loadLattice(){

	int l = (int) (L+0.5L);
	std::string fpath = warmLatPath + std::to_string(l) + "_.lat";
	std::ifstream ifs(fpath.c_str(),std::ios::binary);
	long double ld_read;
	long int li_read;
	bool bool_read;
	std::string str_read;
	if (ifs){
		//load theLattice
		for (int i = 0; i < L; ++i){
			for (int j = 0; j < L; ++j){
				for (int k = 0; k < L; ++k){
					ifs.read(reinterpret_cast<char*>(&ld_read),sizeof(ld_read));
					theLattice[i][j][k] = ld_read;
				}
			}
		}
		//load long doubles
		ifs.read(reinterpret_cast<char*>(&ld_read),sizeof(ld_read));
		L= ld_read;
		ifs.read(reinterpret_cast<char*>(&ld_read),sizeof(ld_read));
		Neqsweeps= ld_read;
		ifs.read(reinterpret_cast<char*>(&ld_read),sizeof(ld_read));
		NTotSweeps= ld_read;
		ifs.read(reinterpret_cast<char*>(&ld_read),sizeof(ld_read));
		maxE= ld_read;
		ifs.read(reinterpret_cast<char*>(&ld_read),sizeof(ld_read));
		beta= ld_read;
		//load long ints
		ifs.read(reinterpret_cast<char*>(&li_read),sizeof(li_read));
		Neqclusts = li_read;
		ifs.read(reinterpret_cast<char*>(&li_read),sizeof(li_read));
		NTotClusts = li_read;
		//load bools
		ifs.read(reinterpret_cast<char*>(&bool_read),sizeof(bool_read));
		coldstart = bool_read;
		ifs.read(reinterpret_cast<char*>(&bool_read),sizeof(bool_read));
		warmedUp = bool_read;
		//load strings
		size_t sz1;
		size_t sz2;
		std::string str1;
		std::string str2;

		ifs.read(reinterpret_cast<char*>(&sz1),sizeof(sz1));
		str1.resize(sz1);
		ifs.read(&str1[0],sz1);

		ifs.read(reinterpret_cast<char*>(&sz2),sizeof(sz2));
		str2.resize(sz2);
		ifs.read(&str2[0],sz2);

		warmLatPath = str1;
		maxEPath = str2;
		
		//recreate other quants
		Nspins = L*L*L;
		updateQuants();//sets energy and mag
		PROB = 1.0L - exp(-2.0L*beta);
		int_L = (int) (L+0.5L);

	}
}
