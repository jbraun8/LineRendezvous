from optimize_params import set_globals, complete_optimization
import sys
import matplotlib.pyplot as plt
import numpy as np

def get_range(max_moves):
	
	vals = []
	fun_vals = []	

	for element in range(max_moves):
		param_id = 1
		n = element + 1
		which_metric = 0
 
		set_globals(param_id, n, which_metric)
		[val,fun_val] = complete_optimization()
		val = val[0]
		vals.append(val)
		fun_vals.append(fun_val)
	
	domain = [x+1 for x in range(max_moves)]
	#plt.scatter(domain, vals)
	#plt.plot(domain, vals)
	plt.scatter(domain, fun_vals)
	plt.plot(domain, fun_vals)
	plt.ylabel('l(n)')
	plt.xlabel('n')
	#plt.ylabel('Optimal X')
	plt.grid(b=True,which='both')
	plt.xticks(domain)
	plt.yticks(np.arange(1.5,4.5,step=0.25))
	plt.show()
	print(vals)
	print(fun_vals)
	return vals	

if __name__ == "__main__":
	get_range(int(sys.argv[1]))
	
