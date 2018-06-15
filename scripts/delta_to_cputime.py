# seconds/old_N = 0.15*L^2.96
# we have delta(N=cpurun)
# to get cpuhours for given delta, first determine N required

# delta ~ 1/sqrt(N)

# old_delta/new_delta = sqrt(old_N)/sqrt(new_N)
# new_N = ( sqrt(old_N) * new_delta/old_delta)^2

# then use scaling of cpuhours/old_N to get cpuhours
import sys

def delta_of_size(L):
    if L == 4:
        return 0.000711445118569810006081688414
    if L == 8:
        return 0.000711445118569810006081688414
    if L == 16:
        return 0.00031621537335898219304303191
    if L == 32:
        return 0.000178227880441284995726228257 
    if L == 64:
        delta = 0.00001785268602218866609
        Nmc =12987.000000000000000000000000000000
        return delta*pow(Nmc/10,0.5)
    if L == 128:
        delta =0.000178227880441284995726228257
        Nmc =3747.02000000000000000000000000000000
        return delta*pow(Nmc/10,0.5)

def cpusec_per_N(L):
    return 0.15584*pow(L, 2.96398)

def calc_cpuhours(L, desired_delta):
    new_N = pow(delta_of_size(L) / desired_delta, 2)
    new_sec = cpusec_per_N(L) * new_N
    return new_sec/(60*60.0)

print(calc_cpuhours(float(sys.argv[1]), float(sys.argv[2])))
