//This program performs montecarlo with the Wolff algorithm simulation of the 3D XY model at the critical temperature
//1/Tc = 0.45416
//taking the system size L as input and outputting binder parameter, db/dt and xi
//
//Implements histogramextrapolation to obtain values at different temperatures
#include <iostream>
#include <cmath>
#include <random>
#include <functional>
#include <sys/syscall.h>
#include <unistd.h>
#include <linux/random.h>
#include <iomanip>
#include <utility>
#include <tuple>

using namespace std;

//print the lattice
void printLattice(double***lattice,double&L){
	cout << "//////////////////" << endl;
	for (int i = 0; i<L; ++i){
		for (int j = 0; j<L; ++j){
			for (int k = 0; k<L; ++k){
				cout << lattice[i][j][k] << " ";
			}
			cout << endl;
		}
		cout << endl;
	}
}
//print cluster
void printCluster(bool***lattice,double&L){
	cout << "//////////////////" << endl;
	for (int i = 0; i<L; ++i){
		for (int j = 0; j<L; ++j){
			for (int k = 0; k<L; ++k){
				cout << lattice[i][j][k] << " ";
			}
			cout << endl;
		}
		cout << endl;
	}
}
int sumCluster(bool***cluster,double &L){
	int sum = 0;
	for (int i = 0; i<L; ++i){
		for (int j = 0; j<L; ++j){
			for (int k = 0; k<L; ++k){
				sum += (int)cluster[i][j][k];
			}
		}
	}
	return sum;
}

//clear the cluster
void emptyCluster(bool***cluster,double &L){
	int steps = 0;
	for (int i = 0; i< L; ++i){
		for (int j = 0; j< L; ++j){
			for (int k = 0; k<L; ++k){	
				cluster[i][j][k] = 0;
			}
		}
	}
}



//calculates the energy of a site
double siteEnergy(double *** lattice,double &L, int &s1, int &s2, int &s3,double&angle){
	double sum = 0;
	//find indices of neighbours
	int n1m = (s1 -1 + (int)L )%(int)L;
	int n1p = (s1 +1 + (int)L )%(int)L;
	int n2m = (s2 -1 + (int)L )%(int)L;
	int n2p = (s2 +1 + (int)L )%(int)L;
	int n3m = (s3 -1 + (int)L )%(int)L;
	int n3p = (s3 +1 + (int)L )%(int)L;
	sum -= cos(angle-lattice[n1m][s2][s3]);
	sum -= cos(angle-lattice[n1p][s2][s3]);
	sum -= cos(angle-lattice[s1][n2m][s3]);
	sum -= cos(angle-lattice[s1][n2p][s3]);
	sum -= cos(angle-lattice[s1][s2][n3m]);
	sum -= cos(angle-lattice[s1][s2][n3p]);
	return sum;
}
//calculate sin(theta - theta_x) upwards +, downward -
double sinX(double ***lattice,double &L, int &s1, int &s2, int &s3,double &angle){
	int np = (s1 + 1) %(int)L;
	int nm = (s1 -1 + (int)L) % (int)L;	
	double ret = 0;
	ret = sin(lattice[nm][s2][s3] - angle) + sin(angle - lattice[np][s2][s3]);
	return ret;
}


//testing functions
double calcSinX(double ***lattice,double &L){
	double sum = 0;
	for (int i =0; i< L; ++i){
		for (int j =0; j< L ; ++j){
			for (int k = 0; k<L; ++k){
				sum += sin(lattice[i][j][k] - lattice[(i+1)%(int)L][j][k]);
			}
		}
	}
	return sum;
}
double calcXMag(double ***lattice,double&L){
	double ret = 0;
	for (int i = 0; i<L; ++i){
		for (int j = 0; j<L; ++j){
			for (int k = 0; k<L; ++k){
				ret += cos(lattice[i][j][k]);
			}
		}
	}
	return ret;
}
double calcYMag(double ***lattice,double&L){
	double ret = 0;
	for (int i = 0; i<L; ++i){
		for (int j = 0; j<L; ++j){
			for (int k = 0; k<L; ++k){
				ret += sin(lattice[i][j][k]);
			}
		}
	}
	return ret;
}

double calcMag(double ***lattice,double&L){
	double mag = sqrt(pow(calcXMag(lattice,L),2) + pow(calcYMag(lattice,L),2));
	return mag;
}	

double calcEn(double ***lattice,double&L){
	double en = 0;
	for (int i = 0; i< L; ++i){
		for (int j = 0; j< L; ++j){
			for (int k = 0; k<L; ++k){	
				en += siteEnergy(lattice,L,i,j,k,lattice[i][j][k]);
			}
		}
	}
	en = 0.5*en;
	return en;
}

//make a cluster..
int growCluster(double &u,int &s1,int &s2,int &s3,double ***lattice,bool ***cluster, double &L,double &beta, auto &randgen,double& TotXMag,double& TotYMag,double& TotEn,double &TotSinX){
	int time = 1;
	//reflect spin and mark as part of cluster
	// 
	double angleBefore = lattice[s1][s2][s3];
	double enBefore = siteEnergy(lattice,L,s1,s2,s3,angleBefore);
	double angleAfter = M_PI + 2*u - angleBefore;
	lattice[s1][s2][s3] = angleAfter;
	cluster[s1][s2][s3] = 1;
	TotEn += siteEnergy(lattice,L,s1,s2,s3,angleAfter) - enBefore;
	TotXMag += cos(angleAfter) - cos(angleBefore);
	TotYMag += sin(angleAfter) - sin(angleBefore);
	TotSinX += sinX(lattice,L,s1,s2,s3,angleAfter) - sinX(lattice,L,s1,s2,s3,angleBefore);
	//
	//find indices of nearest neighbours
	int n1m = (s1 -1 + (int)L )%(int)L;
	int n1p = (s1 +1 + (int)L )%(int)L;
	int n2m = (s2 -1 + (int)L )%(int)L;
	int n2p = (s2 +1 + (int)L )%(int)L;
	int n3m = (s3 -1 + (int)L )%(int)L;
	int n3p = (s3 +1 + (int)L )%(int)L;
	//add them to perimeter list
	tuple<int,int,int,double> perimeter[(int)(L*L*L*6)] = {};
	//index at which we want to add another perimeter spin
	//so if it is equal to 0, it means the list is empty
	//consequently the index of the last spin is n-1
	int n = 0;
	perimeter[n] = make_tuple(n1m,s2,s3,angleAfter); n +=1;
	perimeter[n] = make_tuple(n1p,s2,s3,angleAfter); n +=1;
	perimeter[n] = make_tuple(s1,n2m,s3,angleAfter); n +=1;
	perimeter[n] = make_tuple(s1,n2p,s3,angleAfter); n +=1;
	perimeter[n] = make_tuple(s1,s2,n3m,angleAfter); n +=1;
	perimeter[n] = make_tuple(s1,s2,n3p,angleAfter); n +=1;

	tuple<int,int,int,double> current;
	double prob = 0;
	while (n > 0){
		//pick out the last element 
		current = perimeter[n-1];
		n -= 1;

		//test that it is not already part of cluster
		if (cluster[get<0>(current)][get<1>(current)][get<2>(current)] == 0){
			//increase time for every tested spin
			++time;
			//get angle and energy before reflecting
			angleBefore = lattice[get<0>(current)][get<1>(current)][get<2>(current)];
			//calculate prob of freezing 
			prob = 1 - exp(2*beta*(cos(get<3>(current) - u)*cos(angleBefore -u)));
			//add this perimeter spin to the cluster with probability prob
			if (randgen() < prob){
				enBefore = siteEnergy(lattice,L,get<0>(current),get<1>(current),get<2>(current),angleBefore);
				//reflect and mark as added to cluster
				angleAfter = M_PI + 2*u - angleBefore;
				lattice[get<0>(current)][get<1>(current)][get<2>(current)] = angleAfter; 
				cluster[get<0>(current)][get<1>(current)][get<2>(current)] = 1;
				//update energy and magnetization
				TotEn += siteEnergy(lattice,L,get<0>(current),get<1>(current),get<2>(current),angleAfter) - enBefore;
				TotXMag += cos(angleAfter) - cos(angleBefore);
				TotYMag += sin(angleAfter) - sin(angleBefore);
				TotSinX += sinX(lattice,L,get<0>(current),get<1>(current),get<2>(current),angleAfter) -sinX(lattice,L,get<0>(current),get<1>(current),get<2>(current),angleBefore) ;

				//find indices of its neighbours
				tuple<int,int,int,double> neig1 = make_tuple((get<0>(current) + 1) % (int)L, get<1>(current),get<2>(current),angleAfter);
				tuple<int,int,int,double> neig2 = make_tuple(((int)L + get<0>(current) - 1) % (int)L, get<1>(current),get<2>(current),angleAfter);
				tuple<int,int,int,double> neig3 = make_tuple(get<0>(current), (get<1>(current) + 1) % (int)L,get<2>(current),angleAfter);
				tuple<int,int,int,double> neig4 = make_tuple(get<0>(current), (get<1>(current) + (int)L - 1) % (int)L,get<2>(current),angleAfter);
				tuple<int,int,int,double> neig5 = make_tuple(get<0>(current), get<1>(current), (1 + get<2>(current))%(int)L,angleAfter);
				tuple<int,int,int,double> neig6 = make_tuple(get<0>(current), get<1>(current), (get<2>(current)+(int)L -1 )%(int)L,angleAfter);
				//if it is not already part of the cluster, add it to perimeter list
				if (cluster[get<0>(neig1)][get<1>(neig1)][get<2>(neig1)] ==0){
					perimeter[n] = neig1;
					n = n + 1;
				}
				if (cluster[get<0>(neig2)][get<1>(neig2)][get<2>(neig2)] ==0){
					perimeter[n] = neig2;
					n = n + 1;
				}
				if (cluster[get<0>(neig3)][get<1>(neig3)][get<2>(neig3)] ==0){
					perimeter[n] = neig3;
					n = n + 1;
				}
				if (cluster[get<0>(neig4)][get<1>(neig4)][get<2>(neig4)] ==0){
					perimeter[n] = neig4;
					n = n + 1;
				}
				if (cluster[get<0>(neig5)][get<1>(neig5)][get<2>(neig5)] ==0){
					perimeter[n] = neig5;
					n = n + 1;
				}
				if (cluster[get<0>(neig6)][get<1>(neig6)][get<2>(neig6)] ==0){
					perimeter[n] = neig6;
					n = n + 1;
				}
			}
		}
	}
	return time;
}

//start new cluster
//choose random u vector and starting spin
//grow cluster from those
//empty the cluster when done
//return time  
int newCluster(double *** lattice, bool***cluster,double &L,double &beta,auto &randgen,double& TotXMag,double& TotYMag,double& TotEn,double &TotSinX){
	double u = 2*M_PI*randgen();
	int s1 = L*randgen();
	int s2 = L*randgen();
	int s3 = L*randgen();
	int time;
	time = growCluster(u,s1,s2,s3,lattice,cluster,L,beta,randgen,TotXMag,TotYMag,TotEn,TotSinX);
	emptyCluster(cluster,L);
	return time;
}

//main
int main(int argc, char* argv[]){
	//set precision of cout
	cout.precision(17);
	//generate random seed from system and initialize random number generator
	unsigned long int s;
	syscall(SYS_getrandom,&s,sizeof(unsigned long int),0);	
	uniform_real_distribution<double> dist(0,1);
	mt19937_64 eng; 
	eng.seed(s);
	auto randgen = bind(dist,eng);

	//set system size and temperature from input arguments
	if (argc < 2){
		cout << "input arguments: L T initM N_equil N_samples" << endl;
		exit(0);
	}
	double L = stod(argv[1]);

	double T = stod(argv[2]);
	double beta = 1/T;

	double initM = stod(argv[3]);
	double N_equil_sweeps = stod(argv[4]);
	double N_equil_steps= N_equil_sweeps*L*L*L;
	double N_samples = 0;

	double TotEn;
	double TotXMag;
	double TotYMag;
	double TotSinX;


	//define and initialize the lattice and cluster
	double ***lattice;
	bool***cluster;
	lattice = new double **[(int)L];
	cluster = new bool**[(int)L];
	for (int i = 0; i< L;++i){
		lattice[i] = new double *[(int)L];
		cluster[i] = new bool*[(int)L];
		for (int j =0;j<L;++j){
			lattice[i][j] = new double[(int)L];
			cluster[i][j] = new bool[(int)L];
		}
	}
	for (int i = 0; i<L;++i){
		for (int j=0; j<L;++j){
			for (int k = 0; k<L; ++k){
				lattice[i][j][k] = 0.5*M_PI;
				cluster[i][j][k] = 0;
			}
		}
	}
	TotEn = -3*L*L*L;
	TotXMag = 0;
	TotYMag = L*L*L; 
	TotSinX = 0;
	//test if energy and mag matches
	/*
	double tsinx = calcSinX(lattice,L);
	cout << tsinx << " " << TotSinX << endl;
	*/
	/*
	   TotMag = sqrt(pow(TotXMag,2) + pow(TotYMag,2));
	   double testEn = calcEn(lattice,L);
	   double testXMag = calcXMag(lattice,L);
	   double testYMag = calcYMag(lattice,L);
	   double testMag = calcMag(lattice,L);
	   cout << TotEn <<" TotEn vs testEn " << testEn << endl;
	   cout << TotXMag <<" TotXMag vs testXMag " << testXMag << endl;
	   cout << TotYMag <<" TotYMag vs testYMag " << testYMag << endl;
	   cout << TotMag <<" TotMag vs testMag " << testMag << endl;
	   */

	//eqilibration 
	int t = 0;
	while (t < N_equil_steps){
		t += newCluster(lattice,cluster,L,beta,randgen,TotXMag,TotYMag,TotEn,TotSinX);
		N_samples += 1;
	}
	//test if matches after equilibration
	/*
	tsinx = calcSinX(lattice,L);
	cout << tsinx << " " << TotSinX << endl;
	*/
	/*
	   testEn = calcEn(lattice,L);
	   testXMag = calcXMag(lattice,L);
	   testYMag = calcYMag(lattice,L);
	   testMag = calcMag(lattice,L);
	   TotMag = sqrt(pow(TotYMag,2) + pow(TotXMag,2));
	   cout << TotEn <<" TotEn vs testEn " << testEn << endl;
	   cout << TotXMag <<" TotXMag vs testXMag " << testXMag << endl;
	   cout << TotYMag <<" TotYMag vs testYMag " << testYMag << endl;
	   cout << TotMag <<" TotMag vs testMag " << testMag << endl;
	   */
	//start collecting data

	//parameters and physical quantities
	//averages
	double avgE = 0; //energy
	double avgE2 = 0;//squared energy
	double avgM = 0; //abs of magnetization
	double avgM2 = 0;//squared magnetization
	double avgM4 = 0;//fourth power of magnetization
	double avgM2E = 0;// squared magnetization times energy
	double avgM4E = 0; // 4th power magnetization times energy

	double avgSinX2 = 0;



	for ( int i = 0; i < N_samples; ++i){
		//make a cluster
		newCluster(lattice,cluster,L,beta,randgen,TotXMag,TotYMag,TotEn,TotSinX);
		//take sample data
		avgE += TotEn;
		avgE2 += TotEn*TotEn;
		avgM += sqrt(TotXMag*TotXMag + TotYMag*TotYMag);
		avgM2 += TotXMag*TotXMag + TotYMag*TotYMag;
		avgM4 += (TotXMag*TotXMag + TotYMag*TotYMag)*(TotXMag*TotXMag + TotYMag*TotYMag);
		avgM2E += TotEn*(TotXMag*TotXMag + TotYMag*TotYMag);
		avgM4E += TotEn*(TotXMag*TotXMag + TotYMag*TotYMag)*(TotXMag*TotXMag + TotYMag*TotYMag);
		avgSinX2 += TotSinX*TotSinX;

	}
	//calculate quantities of interest
	//derived quantites
	double xi = 0;//susceptibility
	double b = 0; //Binder parameter
	double dbdt = 0;//derivative wrt T of Binder parameter
	double rs = 0;//superfluid density

	//normalize

	avgE /= N_samples;
	avgE2 /= N_samples;
	avgM /= N_samples;
	avgM2 /= N_samples;
	avgM4 /= N_samples;
	avgM2E /= N_samples;
	avgM4E /= N_samples;
	avgSinX2 /= N_samples;

	//calculate
	b = avgM4;
	b /= (avgM2*avgM2);
	dbdt = (avgM4E/(avgM2*avgM2) + 2*avgM4*avgE/(avgM2*avgM2) - 3*avgM4*avgM2E/(avgM2*avgM2*avgM2));
	dbdt /= (T)*(T);
	xi = avgM2 - avgM*avgM;
	xi /= L*L*L*(T);
	rs = -(1/3)*avgE - beta*avgSinX2;
	rs /= L*L;

	cout << fixed << L << " ";
	cout << fixed << T << " ";
	cout << fixed << avgE/(L*L*L) << " ";
	cout << fixed << avgM/(L*L*L) << " ";
	cout << fixed << b << " ";
	cout << fixed << dbdt << " ";
	cout << fixed << xi << " ";
	cout << fixed << N_equil_sweeps << " ";
	cout << fixed << rs << " ";
	cout << fixed << endl;
}
