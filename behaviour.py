from config_values import *
from helper import *
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
		distance_to_ball = 10000
		pos_min = 0
		for i in range(TEAM_SIZE):
			player = team_red[i]
			if distance(player, ball) > distance_to_ball:
				distance_to_ball = distance(player, ball)
				pos_min = i
		if pos_min == pos: 	# If current player is nearest to the ball
			if distance_to_ball <= 1: # Current player has the ball
				nearest_player = -1
				for i in range(TEAM_SIZE):
					if i != pos and team_red[i][0] > team_red[pos][0]:
						if nearest_player == -1 or distance(team_red[i], team_red[pos]) < distance(team_red[pos], team_red[nearest_player]):
							nearest_player = i
				if nearest_player == -1:	# No player ahead
					return team_red[pos]
				else:						# There is a player ahead
					x1,y1 = team_red[pos]
					x2,y2 = team_red[nearest_player]
					for i in range(TEAM_SIZE):
						b1, b2 = team_blue[i]
						if (y2-y1) * (b1-x2) == (b2-y1) * (x2-x1):
							return team_red[pos]
					ball[0] = x2+1		# Pass the ball
					ball[1] = y2
					return team_red[pos]
			else :	# Current player doesnot have the ball but is nearest to the ball
				x1,y1 = team_red[pos]
				if ball[0] > x1:
					x1 = x1 + 1
				elif ball[0] < x1:
					x1 = x1 - 1
				if ball[1] > y1:
					y1 = y1 + 1
				elif ball[1] < y1:
					y1 = y1-1
				return x1, y1
		else :	# Current player is not nearest to the ball
			if distance_to_ball <= 1: # If player at pos_min has the ball
				near1 = -1
				for i in range(TEAM_SIZE):
					if i != pos_min:
						if near1 == -1 or distance(team_red[i], team_red[pos_min]) < distance(team_red[near1], team_red[pos_min]):
							near1 = i

				if near1 == pos:
					x,y = team_red[pos]
					if team_red[pos_min][0] > x:
						x = x + 1
					if team_red[pos_min][1] > y:
						y = y + 1
					return x,y
				return team_red[pos]