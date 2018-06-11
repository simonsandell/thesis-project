# seconds/old_N = 0.15*L^2.96
# we have delta(N=cpurun)
# to get cpuhours for given delta, first determine N required

# delta ~ 1/sqrt(N)

# old_delta/new_delta = sqrt(old_N)/sqrt(new_N)
# new_N = ( sqrt(old_N) * new_delta/old_delta)^2

# then use scaling of cpuhours/old_N to get cpuhours
import sys

def delta_of_size(L):
    return 0.00172418*pow(L, -0.650472)

def cpusec_per_N(L):
    return 0.15584*pow(L, 2.96398)

def calc_cpuhours(L, desired_delta):
    new_N = 10*pow(delta_of_size(L) / desired_delta, 2)
    new_sec = cpusec_per_N(L) * new_N
    return new_sec/60.0

print(calc_cpuhours(float(sys.argv[1]), float(sys.argv[2])))
