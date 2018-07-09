import numpy as np


import settings
import subtractionMethod


results = np.load(settings.pickles_path + '2L_log_omega/results_jul_5.npy')
subtractionMethod.plot_results_two_l_log(results)

