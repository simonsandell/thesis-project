#ifndef IOFUNCS_H
#define IOFUNCS_H

void printOutput(long double L,long double T, long double E, long double M, long double bin, long double dbdt,long double xi,long double rs, long double N_eq_sweeps, int N_eq_clusts,long double N_samp_sweeps, int N_samp_clusts,bool cold);

long double getMaxE(long double L);

void setMaxE(long double L,long double newE);

void saveLattice(long double L,long double Neqsw,long double Neqcl,long double *** lattice);

long double ***getLattice(long double L,long double&Neqsw,long double&Neqcl);



#endif
