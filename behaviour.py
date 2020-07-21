from config import *

class Behaviour:
	def __init__(self):
		print('')
	def next(self, i, j):
		if i+1 < LENGTH:
			return i+1, j
		elif i-1 >= 0:
			return i-1, j
		return i,j
