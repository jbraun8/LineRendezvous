from main import get_expectation
import matplotlib.pyplot as plt
import sys

def make_plot(num_moves_UB, params):
	
	domain = []
	rangeLB = []
	rangeUB = []
	rangeLB_smart = []
	rangeUB_smart = []

	for i in range(num_moves_UB):
		value = i + 1
		[distribution, LB, UB, LB_smart, UB_smart] = get_expectation(value, params)
		domain.append(value)
		rangeLB.append(LB)
		rangeUB.append(UB)
		rangeLB_smart.append(LB_smart)
		rangeUB_smart.append(UB_smart)
		
		if LB > 4.2575:
			break

	plt.scatter(domain, rangeLB)
	plt.plot(domain, rangeLB)
	plt.scatter(domain, rangeUB)
	plt.plot(domain, rangeUB)
	#plt.scatter(domain, rangeLB_smart)
	#plt.plot(domain, rangeLB_smart)
	plt.scatter(domain, rangeUB_smart)
	plt.plot(domain, rangeUB_smart)
	plt.xlabel('n')
	plt.ylabel('Value of Metric')
	print(rangeUB_smart)
	print(rangeLB)
	plt.show()		




if __name__ == "__main__":
	num_moves_UB = int(sys.argv[1])
	params = (int(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]))
	make_plot(num_moves_UB, params)
