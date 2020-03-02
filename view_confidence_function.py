import sys
import matplotlib.pyplot as plt
import numpy as np
from confidence_function import conf

def plot_conf(params):

	domain = [x * 0.01 for x in range(0,100)]
	values = []
	for element in domain:
		values.append(conf(element, params))
	
	plt.scatter(domain, values)
	plt.plot(domain, values)
	plt.grid(b=True, which='both')
	plt.xticks(np.arange(0,1.1,step=0.1))
	plt.yticks(np.arange(0,1.1,step=0.1))
	plt.show()

if __name__ == "__main__":
	plot_conf([int(sys.argv[1]), float(sys.argv[2])])
