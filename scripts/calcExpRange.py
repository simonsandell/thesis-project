from analysis import calc_exponent

W_FROM_3LBIN = 0.62
W_FROM_EXPONENT_FIT = 0.782566
W_ANALYTIC = 1.0
# orange = np.linspace(w_from_exponent_fit*0.9,w_from_exponent_fit*1.1,11);
ORANGE = [W_FROM_3LBIN, W_FROM_EXPONENT_FIT, W_ANALYTIC]
NRANGE = [0, 1, 2]
for o in ORANGE:
    for n in NRANGE:
        calc_exponent.calculate_exponents(o, n)
        print(o,n)
