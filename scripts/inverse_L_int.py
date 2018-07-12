import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

def line(x, k, m):
    y = k*x +m;
    return y

b_int = [2.20177444, 2.201843]
L = [1, 0.5]

params,covar = curve_fit(line, L, b_int)

X = np.linspace(0, 2, 50)
Y = line(X,params[0], params[1])
plt.plot(X,Y)
plt.title(str(line(0, params[0], params[1])))
plt.show()

