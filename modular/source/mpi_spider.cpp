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
	std::cout << "WORLD_rank" << world_rank<< std::endl;


	if (world_rank != 0){
		_3DXY::wolffHistJob(4.0L);
	}
	else{
		int N_finished =0;
		while (true){
			int char_amount;
			MPI_Status status;
			MPI_Probe (MPI_ANY_SOURCE,MPI_ANY_TAG,MPI_COMM_WORLD, &status);
			MPI_Get_count(&status,MPI_CHAR,&char_amount);
			char *buf = (char*)malloc(sizeof(char)*char_amount);
			MPI_Recv(buf,char_amount,MPI_CHAR,MPI_ANY_SOURCE,MPI_ANY_TAG,MPI_COMM_WORLD, MPI_STATUS_IGNORE);
			std::cout << buf;
			if (status.MPI_TAG != 0){
				N_finished +=1;
				if (N_finished > (world_size -2)){
					break;
				}
			}

		}
	}
	MPI_Finalize();
}

