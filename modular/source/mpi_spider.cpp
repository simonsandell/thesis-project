#include <mpi.h>
#include <stdio.h>
#include <string.h>
#include <iostream>
#include <limits>

#include "clusterStruct.h"
#include "randStruct.h"

#include "Ising3D.h"
#include "3DXY.h"

long double argToL(const char* l){
	if(strcmp(l,"4")==0){
		return 4.0L;
	}
	if(strcmp(l,"8")==0){
		return 8.0L;
	}
	if(strcmp(l,"16")==0){
		return 16.0L;
	}
	if(strcmp(l,"32")==0){
		return 32.0L;
	}
	if(strcmp(l,"64")==0){
		return 64.0L;
	}
	if(strcmp(l,"128")==0){
		return 128.0L;
	}
	exit(-1);
	return -999999999999999999.0L;
}


int main(int argc,char* argv[]){
	if(argc != 2){
		std::cout << "# bad input"<< std::endl;
		exit(-1);
	}
	long double L = argToL(argv[1]);
	typedef std::numeric_limits<long double> dbl;
	std::cout.precision(dbl::max_digits10 + 5);

	MPI_Init(NULL,NULL);

	int world_size;
	MPI_Comm_size(MPI_COMM_WORLD,&world_size);

	int world_rank;
	MPI_Comm_rank(MPI_COMM_WORLD,&world_rank);

	std::cout << "WORLD_SIZE " << world_size << std::endl;
	std::cout << "WORLD_rank " << world_rank<< std::endl;

	std::string b_pwd = "/cfs/klemming/scratch/s/simsan/"; 
	std::string h_pwd = "/home/simon/exjobb/modular/"; 
	std::string o_pwd = "/home/simsan/exjobb/modular/"; 

	std::string env = h_pwd;
	std::string model = "3DXY/";

	std::string mep= env + "maxE/" + model; 
	std::string wlp= env + "warmLattice/" + model; 
	bool doP = false;

	if (world_rank != 0){
		if (world_rank == 1){
			doP = true;
		_3DXY::correlationRun(mep, wlp, L);
		std::string bigstr = "# finished\n";
		int tag = 1;
		MPI_Send(bigstr.c_str(),bigstr.size(),MPI_CHAR,0,tag,MPI_COMM_WORLD);
                }
	}
	if (world_rank == 0){
		int N_finished = 0;
		while (true){
			int char_amount;
			MPI_Status status;
			MPI_Probe(MPI_ANY_SOURCE,MPI_ANY_TAG,MPI_COMM_WORLD, &status);
			MPI_Get_count(&status,MPI_CHAR,&char_amount);
			char *buf = (char*)malloc(sizeof(char)*(char_amount+1));
			MPI_Recv(buf,char_amount,MPI_CHAR,MPI_ANY_SOURCE,MPI_ANY_TAG,MPI_COMM_WORLD, MPI_STATUS_IGNORE);
			if (status.MPI_TAG == 1 || status.MPI_TAG == 0){

				std::cout.write(buf,sizeof(char)*(char_amount));
			}
			if (status.MPI_TAG == 1){
				N_finished +=1;
				if (N_finished == (world_size - 1)){
					break;
				}
			}
		}
	}
	MPI_Finalize();
}

