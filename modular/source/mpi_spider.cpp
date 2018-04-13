#include <mpi.h>
#include <iostream>

#include "clusterStruct.h"
#include "randStruct.h"

#include "Ising3D.h"
#include "3DXY.h"

int main(){

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
	
	std::string choice = b_pwd;
	std::string model = "3DXY/";
		  
	std::string mep= choice + "maxE/" + model; 
	std::string wlp= choice + "warmLattice/" + model; 

	if (world_rank != 0){
		_3DXY::warmupJob(64.0L,mep,wlp);
		std::string endmsg = "finished";	
		MPI_Send(endmsg.c_str(),endmsg.size(),MPI_CHAR,0,1,MPI_COMM_WORLD);
	}
	else{
		int N_finished =0;
		while (true){
			int char_amount;
			MPI_Status status;
			MPI_Probe (MPI_ANY_SOURCE,MPI_ANY_TAG,MPI_COMM_WORLD, &status);
			MPI_Get_count(&status,MPI_CHAR,&char_amount);
			char *buf = (char*)malloc(sizeof(char)*(char_amount+1));
			MPI_Recv(buf,char_amount,MPI_CHAR,MPI_ANY_SOURCE,MPI_ANY_TAG,MPI_COMM_WORLD, MPI_STATUS_IGNORE);
			if (status.MPI_TAG == 1 || status.MPI_TAG == 0){
				std::cout << "before mpi_rev message" << std::endl;
				std::cout.write(buf,sizeof(char)*(char_amount+1));
				std::cout << "after mpi_rev message" << std::endl;
			}
			if (status.MPI_TAG == 1){
				N_finished +=1;
				if (N_finished > (world_size -2)){
					break;
				}
			}
		}
	}
	MPI_Finalize();
}

