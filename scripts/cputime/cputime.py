from scipy.optimize import curve_fit

total_mcs = [
1.01*1.08*(10**11),
1.01*7.63*(10**10),
1.01*2.25*(10**10),
1.01*1.76*(10**10),
1.01*1.63*(10**9),
1.1*6.91*(10**8),
]
sec_for_1m = [
    92.218,
    718.07,
    5782.3,
    45072,
]
def f(L, a0,a1):
    return (a0*(L**a1))
params, covar = curve_fit(f, [4, 8, 16, 32], sec_for_1m)
sec_for_1m.append(f(64, params[0], params[1]))
sec_for_1m.append(f(128, params[0], params[1]))

tmcs_div = [x/(10**6) for x in total_mcs]

total_secs = [x*y for x,y in zip(tmcs_div, sec_for_1m)]
total_hs = [x/(60*60) for x in total_secs]
print(total_hs)
print(sum(total_hs)/1000)
print(params)
require = 425000;
c = require/sum(total_hs)
print([c*x for x in total_hs])
