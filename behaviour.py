from config_values import *
import random

class Behaviour:
	def __init__(self):
		print('')
	def next(self, i, j):
		return i,j

class Random(Behaviour):
	def __init__(self):
		super().__init__()
	def next(self, pos, team_red, team_blue, ball):
		rand_num = random.random()
		step = 0
		x = 0 
		y = 0
		if rand_num < 0.5:
			step = -10
		else:
			step = 10
		x = team_blue[pos][0] + step

		rand_num = random.random()
		step = 0
		if rand_num < 0.5:
			step = -10
		else:
			step = 10
		y = team_blue[pos][1] + step

		return x, y

class RuleBased(Behaviour):
	def __init__(self):
		super().__init__()
	def next(self, pos, team_red, team_blue, ball):
		return team_red[pos]