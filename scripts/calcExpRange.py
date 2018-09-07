from analysis import calc_exponent


W = 0.820
# orange = np.linspace(w_from_exponent_fit*0.9,w_from_exponent_fit*1.1,11);
#ORANGE = [W_FROM_3LBIN, W_FROM_EXPONENT_FIT, W_ANALYTIC]
ORANGE = [W]
NRANGE = [0, 1, 2]
for o in ORANGE:
    for n in NRANGE:
        calc_exponent.calculate_exponents(o, n)
        print(o,n)
