#from scipy.optimize import Bounds
from scipy.optimize import minimize
import numpy as np
from main import get_expectation
import sys


def objective_function(param):

	[distributions, LB, UB, LB_smart, UB_smart] = get_expectation(N, [PARAM_ID, param[0], 0])

	if WHICH_METRIC == 0:
		return LB
	else:
		return UB_smart

def complete_optimization():
	
	#bounds = Bounds([1,2])
	x0 = np.array([1.5])
	res = minimize(objective_function, x0, method = 'Nelder-Mead',options={'disp': True})
	print(res.x)
	
	return [res.x,res.fun]


def set_globals(param_id, n, which_metric):
	
	global N 
	N = n
	global PARAM_ID
	PARAM_ID = param_id
	global WHICH_METRIC 
	WHICH_METRIC = which_metric
	
	return True 	

if __name__ == "__main__":
	PARAM_ID = int(sys.argv[1])
	N = int(sys.argv[2])
	WHICH_METRIC = int(sys.argv[3])
	complete_optimization()


