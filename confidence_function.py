# confidence function script
# always returns number between 0 and 1
# 0.5 always maps to 0.5
import numpy as np
import math

def conf(value,params):	
	
	if int(params[0]) == 0:
	# Alpern's Original Strategy	
		if value == 0.5:
			return 0.5
		elif value > 0.5:
			return 1
		else:
			return 0

	elif int(params[0]) == 1:
	# Linear Confidence Mapping
		if value >= 0.5:
			output = float(params[1]) * (np.sin (value - 0.5))/(value) + 0.5
		else:
			output = 1 - conf(1 - value,params)

		if output > 1:
			return 1
		elif output < 0:
			return 0
		else:
			return output 
	
	elif int(params[0]) == 2:
	# Sigmoid
		if value >= 0.5:
			if value >= 0.6516325:
				output = ((1 - params[1])/(0.803265 - 0.6516325))*(value - 0.6516325) + params[1]
			else:
				output = ((params[1] - 0.5)/(0.6516325 - 0.5))*(value - 0.5) + 0.5			

		else:
			output = 1 - conf(1 - value,params)
		if output > 1:
			return 1
		elif output < 0:
			return 0
		else:
			return output

	else:
		return 0	
	
