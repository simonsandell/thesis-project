#include <iostream>
#include <string>
#include <sstream>
#include <unistd.h>
#include <random>
#include <sys/syscall.h>
#include <fstream>
#include <cstring>
#include <cerrno>
#include <tuple>

#include "3DXYlattice.h"
#include "3DXYio.h"
#include "../maxEHandle.h"



long unsigned int xyzToK( int x, int y , int z,long double L){
	long unsigned int ret = 0;
	ret += (long unsigned int) x;
	ret += (long unsigned int) (y*L);
	ret += (long unsigned int) (z*L*L);
	return ret;
}

std::tuple<int,int,int> Lattice3DXY::kToXYZ(unsigned long int K){
	int x = K % int_L;
	int yL = (K-x)%(int_L*int_L);
	int zLL = (K-x-yL);
	int y = int((yL+0.1)/int_L);
	int z = int((zLL+0.1)/(int_L*int_L));
	std::tuple<int,int,int> ret = std::make_tuple(x,y,z);
	return ret;
}

void Lattice3DXY::print_lattice(){
    for (int i =0; i< L; i++){
        for (int j = 0; j<L; j++){
            for (int k = 0; k<L; k++){
                std::cout << i << j << k << std::endl;
                std::cout << theLattice[xyzToK(i,j,k,L)] << std::endl;
            }
        }
    }
}

long double Lattice3DXY::siteEnergy( unsigned long int K){
	long double sum = 0.0L;
	for (long unsigned int n =0; n<6; ++n){
		sum -= cos(theLattice[K] - theLattice[Neighbours[K][n]]);
	}
	return sum;
}
//calculate sin(theta - theta_x) upwards +, downward -
long double Lattice3DXY::sinX(unsigned long int &K,long double &angle){
	long double ret = sin(theLattice[Neighbours[K][0]] - angle) + sin(angle - theLattice[Neighbours[K][1]]);
	return ret;
}
long double Lattice3DXY::sinY(unsigned long int &K,long double &angle){
	long double ret = sin(theLattice[Neighbours[K][2]] - angle) + sin(angle - theLattice[Neighbours[K][3]]);
	return ret;
}
long double Lattice3DXY::sinZ(unsigned long int &K,long double &angle){
	long double ret = sin(theLattice[Neighbours[K][4]] - angle) + sin(angle - theLattice[Neighbours[K][5]]);
	return ret;
}

long double calcSinX(long double *lattice,long double  L){
	long double sum = 0.0L;
	int intel = (int)(L+0.5L);
	for (int i =0; i< L; ++i){
		for (int j =0; j< L ; ++j){
			for (int k = 0; k<L; ++k){
				sum += sin(lattice[xyzToK(i,j,k,L)] - lattice[xyzToK((i+1)%intel,j,k,L)]);
			}
		}
	}
	return sum;
}
long double calcSinY(long double *lattice,long double  L){
	long double sum = 0.0L;
	int intel = (int)(L+0.5L);
	for (int i =0; i< L; ++i){
		for (int j =0; j< L ; ++j){
			for (int k = 0; k<L; ++k){
				sum += sin(lattice[xyzToK(i,j,k,L)] - lattice[xyzToK(i,(j+1)%intel,k,L)]);
			}
		}
	}
	return sum;
}
long double calcSinZ(long double *lattice,long double  L){
	long double sum = 0.0L;
	int intel = (int)(L+0.5L);
	for (int i =0; i< L; ++i){
		for (int j =0; j< L ; ++j){
			for (int k = 0; k<L; ++k){
				sum += sin(lattice[xyzToK(i,j,k,L)] - lattice[xyzToK(i,j,(k+1)%intel,L)]);
			}
		}
	}
	return sum;
}

long double calcXMag(long double *lattice,long double L){
	long double ret = 0.0L;
	for (int i = 0; i<L; ++i){
		for (int j = 0; j<L; ++j){
			for (int k = 0; k<L; ++k){
				ret += cos(lattice[xyzToK(i,j,k,L)]);
			}
		}
	}
	return ret;
}
long double calcYMag(long double *lattice,long double L){
	long double ret = 0.0L;
	for (int i = 0; i<L; ++i){
		for (int j = 0; j<L; ++j){
			for (int k = 0; k<L; ++k){
				ret += sin(lattice[xyzToK(i,j,k,L)]);
			}
		}
	}
	return ret;
}

long double calcMag(long double *lattice,long double L){
	long double mag = sqrt(pow(calcXMag(lattice,L),2) + pow(calcYMag(lattice,L),2));
	return mag;
}	

long double calcEn(Lattice3DXY* lat){
	long double en = 0.0L;
	long double ell = lat->L;
	for (int i = 0; i< lat->L; ++i){
		for (int j = 0; j< lat->L; ++j){
			for (int k = 0; k<lat->L; ++k){	
				en += lat->siteEnergy(xyzToK(i,j,k,ell));
			}
		}
	}
	en = 0.5L*en;
	return en;
}
long double* Lattice3DXY::newLattice(long double L,bool cold){
	long unsigned int nspins = (long unsigned int)(L*L*L+0.1L);
	long double* lattice;
	lattice = new long double[nspins];
	//make new lattice
	if (cold) {
		for (long unsigned int i = 0; i<nspins;++i){
			lattice[i] = 0.0L;
		}
	}
	else {
		for (long unsigned int i = 0; i<nspins;++i){
			lattice[i] = rand.rnd()*2.0L*M_PI;
		}
	}
	return lattice;
}
//update quantiites of the lattice
void Lattice3DXY::updateQuants(){
	energy = calcEn(this);
	xmag = calcXMag(theLattice,L);
	ymag = calcYMag(theLattice,L);
	sinx = calcSinX(theLattice,L);
	siny = calcSinY(theLattice,L);
	sinz = calcSinZ(theLattice,L);
};
unsigned long  int ** Lattice3DXY::generateNeighbours(int l){
	std::tuple<int,int,int> xyz;
	long unsigned int n1,n2,n3,n4,n5,n6;
	int x,y,z,x1,x2,y1,y2,z1,z2;
	int nspins = l*l*l;
	unsigned long int **  result = new long unsigned int*[nspins];
	for (int i = 0; i<nspins; ++i){
		xyz = kToXYZ(i);
		x = std::get<0>(xyz);
		y = std::get<1>(xyz);
		z = std::get<2>(xyz);
		x1 = (x+l-1)%l;
		x2 = (x+l+1)%l;
		y1 = (y+l-1)%l;
		y2 = (y+l+1)%l;
		z1 = (z+l-1)%l;
		z2 = (z+l+1)%l;
		n1 = xyzToK(x1,y,z,l);
		n2 = xyzToK(x2,y,z,l);
		n3 = xyzToK(x,y1,z,l);
		n4 = xyzToK(x,y2,z,l);
		n5 = xyzToK(x,y,z1,l);
		n6 = xyzToK(x,y,z2,l);
		result[i]= new unsigned long int[6];
		result[i][0]= n1;
		result[i][1]= n2;
		result[i][2]= n3;
		result[i][3]= n4;
		result[i][4]= n5;
		result[i][5]= n6;
                /*
                std::cout << "k " << i << std::endl;
                std::cout << "xyz" << x << " " << y << " " << z << std::endl;
                std::cout << n1 << " " << n2 << " " << n3 << " " << n4 << " " << n5 << " " << n6 << std::endl;
                */
	}
	return result;
}

//initialize new lattice
Lattice3DXY::Lattice3DXY(int l,long double rT, bool cold,RandStruct r,Cluster c,std::string pathMaxE,std::string pathWarmLat) 
	:  rand(r),clust(c) 

{
	theLattice = newLattice((long double)l,cold);
	runTemp = rT;
	L = (long double)l;
	Nspins =L*L*L;
	int_L = (long int) (L + 0.5L);
	beta = 1.0L/rT;
	Neqsweeps = 0.0L;
	NTotSweeps= 0.0L;
	Neqclusts = 0;
	NTotClusts= 0;
	coldstart = cold;
	warmedUp = false;

	warmLatPath = pathWarmLat;
	maxEPath = pathMaxE;
	Neighbours = generateNeighbours(l);
	maxE = getMaxE(pathMaxE,l);

	if (cold) {
		energy = -3.0L*Nspins;
		xmag = Nspins;
		ymag = 0.0L;
		sinx = 0.0L;
		siny = 0.0L;
		sinz = 0.0L;
	}
	else {
		energy = calcEn(this);
		xmag = calcXMag(theLattice,L);
		ymag = calcYMag(theLattice,L); 
		sinx = calcSinX(theLattice,L);
		siny = calcSinY(theLattice,L);
		sinz = calcSinZ(theLattice,L);
	}


};
Lattice3DXY::Lattice3DXY(){

}

void Lattice3DXY::testConsistent(){

	typedef std::numeric_limits<long double> dbl;
	std::cout.precision(dbl::max_digits10 + 5);
	long double testSinX = calcSinX(theLattice,L);
	long double testSinY = calcSinY(theLattice,L);
	long double testSinZ = calcSinZ(theLattice,L);
	long double testEn = calcEn(this);
	long double testXMag = calcXMag(theLattice,L);
	long double testYMag = calcYMag(theLattice,L);
	long double TotEn = energy;
	long double TotXMag= xmag;
	long double TotYMag= ymag;
	long double TotSinX= sinx;
	long double TotSinY = siny;
	long double TotSinZ = sinz;
	std::cout <<std::fixed<< TotEn - testEn << "  E    "<< TotEn << " "<< testEn << std::endl;
	std::cout <<std::fixed<< TotXMag - testXMag << "  X    "<< TotXMag << " "<< testXMag << std::endl;
	std::cout <<std::fixed<< TotYMag - testYMag << "  Y    "<< TotYMag << " "<< testYMag << std::endl;
	std::cout <<std::fixed<< TotSinX - testSinX << "  Sx    "<< TotSinX << " "<< testSinX << std::endl;
	std::cout <<std::fixed<< TotSinY - testSinY << "  Sy    "<< TotSinY << " "<< testSinY << std::endl;
	std::cout <<std::fixed<< TotSinZ - testSinZ << "  Sz    "<< TotSinZ << " "<< testSinZ << std::endl;
	//new test of magnetization
	long double sitemag;
	long double accum = 0.0L;
	std::cout << "Magnetization at sites: " << std::endl;
	for (int i = 0; i< L; ++i){
		for (int j = 0; j< L; ++j){
			for (int k = 0; k<L; ++k){	
				sitemag = std::pow(sin(theLattice[xyzToK(i,j,k,L)]),2.0L) + 
					std::pow(cos(theLattice[xyzToK(i,j,k,L)]),2.0L);
				std::cout << std::fixed << sitemag << std::endl;
				accum += std::abs(sitemag - 1.0L);
			}
		}
	}
	std::cout << "Accumulated error: ";
	std::cout << std::fixed << accum << std::endl;
}

std::string timetag3dxy(){
	time_t  t = time(0);
	struct tm * now = localtime(& t);

	char buffer [80];
	strftime (buffer,80,"%Y-%m-%d.%H:%M:%S",now);
	std::ostringstream mstream;
	mstream << buffer;  
	return mstream.str();
}
void Lattice3DXY::saveLattice(){
	std::string tt = timetag3dxy();
	saveLatticeAs(tt);
}

void Lattice3DXY::saveLatticeAs(std::string name){
	//save theLattice, runTemp not beta, L not Nspins, Neqsweeps, NTotSweeps,
	//	Neqclusts,NTotClusts,
	//	coldstart, warmedup,
	//	warmLatPath, maxEPath,
	//	maxE
	//
	//	long doubles 
	//	theLattice, runTemp,L,Neqsweeps,NTotSweeps,maxE
	//	long ints
	//	Neqclusts,NTotClusts
	//	bools
	//	coldstart, warmedup
	//	strings
	//	warmLatPath, maxEPath
	//
	//dont save energy,mag, etc, call updateQuants() instead on load
	//
	std::ostringstream fpath;
	fpath << warmLatPath << L << "_" << name << "_.lat";
	std::ofstream ofs(fpath.str().c_str(),std::ios::binary);

	if( ofs){
		//save theLattice
		for (int i = 0; i< L;++i){
			for (int j = 0; j< L;++j){
				for (int k = 0; k< L;++k){
					ofs.write(
							reinterpret_cast<char *>(&theLattice[xyzToK(i,j,k,L)]),
							sizeof(theLattice[xyzToK(i,j,k,L)])
						 );
				}
			}
		}
		//save long doubles
		ofs.write(reinterpret_cast<char*>(& runTemp) , sizeof( runTemp ));
		ofs.write(reinterpret_cast<char*>(& L) , sizeof( L ));
		ofs.write(reinterpret_cast<char*>(& Neqsweeps) , sizeof( Neqsweeps ));
		ofs.write(reinterpret_cast<char*>(& NTotSweeps) , sizeof( NTotSweeps ));
		ofs.write(reinterpret_cast<char*>(& maxE) , sizeof( maxE ));
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
void Lattice3DXY::loadLattice(){
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
					theLattice[xyzToK(i,j,k,L)] = ld_read;
				}
			}
		}
		//load long doubles
		ifs.read(reinterpret_cast<char*>(&ld_read),sizeof(ld_read));
		runTemp = ld_read;
		ifs.read(reinterpret_cast<char*>(&ld_read),sizeof(ld_read));
		L= ld_read;
		ifs.read(reinterpret_cast<char*>(&ld_read),sizeof(ld_read));
		Neqsweeps= ld_read;
		ifs.read(reinterpret_cast<char*>(&ld_read),sizeof(ld_read));
		NTotSweeps= ld_read;
		ifs.read(reinterpret_cast<char*>(&ld_read),sizeof(ld_read));
		maxE= ld_read;
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

		//warmLatPath = str1;
		//maxEPath = str2;

		//recreate other quants
		Nspins = L*L*L;
		beta = 1.0L/runTemp;
		int_L = (long int)(L+0.5L);
		updateQuants();
		//maxE shouldnt have been saved..
		maxE = getMaxE(maxEPath,L);
	}

}
long double Lattice3DXY::getAngle(int s1,int s2,int s3){
	long unsigned int k = xyzToK(s1,s2,s3,L);
	return theLattice[k];
}
void Lattice3DXY::setAngle(int s1,int s2,int s3,long double newAng){
	long unsigned int k = xyzToK(s1,s2,s3,L);
	theLattice[k] = newAng;
}


void Lattice3DXY::printVals(){
	std::cout << "runTemp L, NTotSweeps,NTotClusts, coldstart, warmLatPath ,maxEPath, maxE, energy " << std::endl <<
		runTemp << " " << L << " " << NTotSweeps<< " " <<NTotClusts<< " " << coldstart<< " " << warmLatPath << " " <<maxEPath<< " " << maxE<< " " << energy << std::endl;

}



