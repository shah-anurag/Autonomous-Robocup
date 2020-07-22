from config_values import *

class Behaviour:
	def __init__(self):
		print('')
	def next(self, i, j):
		if i+10 < HEIGHT:
			return i+10, j
		elif i-10 >= 0:
			return i-10, j
		return i,j
