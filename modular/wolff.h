#ifndef WOLFF_H
#define WOLFF_H

#include <functional> 
#include <unistd.h> 
#include <cmath> 
#include <random>
#include <utility>
#include <iomanip>
#include <sys/syscall.h>
using namespace std;

int growCluster(double ***lattice,bool ***cluster, double &L,double &beta, double &(randgen)(),double& TotXMag,double& TotYMag,double& TotEn,double &TotSinX);



#endif
