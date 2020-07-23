from config_values import *
from helper import *
import random

class Behaviour:
	def __init__(self):
		pass
		# print('')
	def next(self, i, j):
		return i,j
	def distance(self, playerA, playerB):
		return abs(playerA[0] - playerB[0]) + abs(playerA[1] - playerB[1])

class Random(Behaviour):
	def __init__(self):
		super().__init__()
	def next(self, pos, team_own, team_opp, ball):
		rand_num = random.random()
		step = 0
		x = 0 
		y = 0
		if rand_num < 0.5:
			step = -10*rand_num*2
		else:
			step = 10*(rand_num-0.5)*2
		x = team_own[pos][0] + step
		if(x>=WIDTH):
			x = x - 10
		if(x<=0):
			x = x + 10
		
		rand_num = random.random()
		step = 0
		if rand_num < 0.5:
			step = -10*rand_num*2
		else:
			step = 10*(rand_num-0.5)*2
		y = team_own[pos][1] + step
		if(y>=HEIGHT):
			y = y - 10
		if(y<=0):
			y = y + 10
		return x, y

class RuleBased(Behaviour):
	def __init__(self):
		super().__init__()
	def next(self, pos, team_own, team_opp, ball):
		distance_to_ball = 10000
		pos_min = 0
		for i in range(TEAM_SIZE):
			player = team_own[i]
			if distance(player, ball) < distance_to_ball:
				distance_to_ball = distance(player, ball)
				pos_min = i
		# print('posmin', pos_min, pos)
		if pos_min == pos: 	# If current player is nearest to the ball
			# print('5.', pos)
			if distance_to_ball <= 1: # Current player has the ball
				if distance(team_own[pos], (WIDTH, HEIGHT/2)) <= 50:
					ball[0] = WIDTH
					ball[1] = HEIGHT/2
					return team_own[pos]
				nearest_player = -1
				for i in range(TEAM_SIZE):
					if i != pos and team_own[i][0] > team_own[pos][0]:
						if nearest_player == -1 or distance(team_own[i], team_own[pos]) < distance(team_own[pos], team_own[nearest_player]):
							nearest_player = i
				# print('nearest Player', nearest_player)
				if nearest_player == -1:	# No player ahead
					return team_own[pos]
				else:						# There is a player ahead
					x1,y1 = team_own[pos]
					x2,y2 = team_own[nearest_player]
					for i in range(TEAM_SIZE):
						b1, b2 = team_opp[i]
						epsilon = 1
						print('Oppponent', (y2-y1) * (b1-x1), (b2-y1) * (x2-x1))
						if (y2-y1) * (b1-x1) <= (b2-y1) * (x2-x1) + epsilon and (b2-y1) * (x2-x1) <= (y2-y1) * (b1-x1) + epsilon:
							# exit(1)
							return team_own[pos]
					ball[0] = x2+1		# Pass the ball
					ball[1] = y2
					return team_own[pos]
			else :	# Current player doesnot have the ball but is nearest to the ball
				# print('4 pos', pos)
				x1,y1 = team_own[pos]
				if ball[0] > x1:
					x1 = x1 + 1
				elif ball[0] < x1:
					x1 = x1 - 1
				if ball[1] > y1:
					y1 = y1 + 1
				elif ball[1] < y1:
					y1 = y1 - 1
				# print('Moving to', x1, y1, 'from', team_own[pos], ball)
				return x1, y1
		else :	# Current player is not nearest to the ball
			if distance_to_ball <= 1: # If player at pos_min has the ball
				# print('1 pos', pos)
				near1 = -1
				for i in range(TEAM_SIZE):
					if i != pos_min:
						if near1 == -1 or distance(team_own[i], team_own[pos_min]) < distance(team_own[near1], team_own[pos_min]):
							near1 = i

				if near1 == pos and team_own[pos][0] <= team_own[pos_min][0] + 20:
					x,y = team_own[pos]
					if team_own[pos_min][0] >= x:
						x = x + 1
					# if team_own[pos_min][1] >= y:
					# 	y = y + 1
					return x,y
				return team_own[pos]
			else:
				# print('3 pos_min', pos_min, 'pos', pos)
				near1 = None
				for i in range(TEAM_SIZE):
					if i != pos_min:
						if near1 == None or distance(team_own[i], team_own[pos_min]) < distance(team_own[pos_min], team_own[near1]):
							near1 = i
				if near1 == pos:
					x, y = team_own[pos]
					if x <= team_own[pos_min][0]:
						x = x + 1
					# if y <= team_own[pos_min][1]:
					# 	y = y + 1
					return x,y
				else:
					return team_own[pos]

class Defensive(Behaviour):
	def __init__(self):
		super().__init__()
	def next(self, pos, team_own, team_opp, ball):
		if distance(team_own[pos], ball) > 1:
			if team_own[pos][0] - ball[0] < 20 or team_own[pos][0]+20 < ball[0]:
				return min(WIDTH, team_own[pos][0]+1), team_own[pos][1]
			else:
				return team_own[pos]

		if distance(team_own[pos], (WIDTH, HEIGHT/2)) <= 50:
			ball[0] = WIDTH
			ball[1] = HEIGHT/2
			return team_own[pos]

		# This player has the ball
		behind = []
		for i in range(TEAM_SIZE):
			if i != pos:
				if team_own[i][0] < team_own[pos][0]:
					inc = True
					x1,y1 = team_own[pos]
					x2,y2 = team_own[i]
					for i in range(TEAM_SIZE):
						b1, b2 = team_opp[i]
						epsilon = 1
						if (y2-y1) * (b1-x2) <= (b2-y1) * (x2-x1) + epsilon and (b2-y1) * (x2-x1) <= (y2-y1) * (b1-x2) + epsilon:
							inc = False
							break
					if inc:
						behind.append(i)
		if len(behind) > 0:
			random.seed(len(behind) * random.random())
			# print(random.randrange(len(behind)))
			passto = team_own[behind[random.randrange(len(behind))]]
			print('passto', passto)
			ball[0] = passto[0]
			ball[1] = passto[1]
		return team_own[pos]