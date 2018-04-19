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
	
	std::string env = o_pwd;
	std::string model = "Ising3D/";
		  
	std::string mep= env + "maxE/" + model; 
	std::string wlp= env + "warmLattice/" + model; 

	if (world_rank != 0){
		bool cold = false;
		Ising3D::teqJob(16.0L,cold,mep,wlp);
		Ising3D::teqJob(8.0L,cold,mep,wlp);
		Ising3D::teqJob(4.0L,cold,mep,wlp);
		std::string bigstr = "\nfinished\n";
		MPI_Send(bigstr.c_str(),bigstr.size(),MPI_CHAR,0,1,MPI_COMM_WORLD);

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
				std::cout.write(buf,sizeof(char)*(char_amount));
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

