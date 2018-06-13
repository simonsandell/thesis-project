import calcExponent

w_from_3LBin = 0.62
w_from_exponent_fit = 0.782566
# orange = np.linspace(w_from_exponent_fit*0.9,w_from_exponent_fit*1.1,11);
orange = [w_from_exponent_fit]
nrange = [0, 1, 2, 3]
for o in orange:
    for n in nrange:
        calcExponent.calculate_exponents(o, n)
