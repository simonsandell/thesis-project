#include <mpi.h>

#include "ThreadPool.h"
#include "clusterStruct.h"
#include "randStruct.h"

#include "Ising3D.h"
#include "3DXY.h"
using namespace std;
int main(){

	MPI_Init(NULL,NULL);

	int world_size;
	MPI_Comm_size(MPI_COMM_WORLD,&world_size);

	int world_rank;
	MPI_Comm_rank(MPI_COMM_WORLD,&world_rank);

	bool cold = true;

	_3DXY::teqRun(4.0L,cold);
	_3DXY::teqRun(8.0L,cold);
	_3DXY::teqRun(16.0L,cold);
	_3DXY::teqRun(32.0L,cold);




	MPI_Finalize();
}

