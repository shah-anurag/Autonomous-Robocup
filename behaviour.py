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
	def isfree(self, x1, y1, x2, y2, team_own, team_opp):
		if x2 == x1:
			x2 = x1+0.001
		m = (y2 - y1) / (x2 - x1)
		c = y2 - m*x2
		for i in range(TEAM_SIZE):
			opp = team_opp[i]
			if (distance((x1,y1), opp) > distance((x1,y1), (x2,y2))) or (distance((x2,y2), opp) > distance((x1,y1), (x2,y2))):
				continue
			step = 50
			corners = [(opp[0]+step, opp[1]+step), (opp[0]+step, opp[1]-step), (opp[0]-step, opp[1]+step), (opp[0]-step, opp[1]-step)]
			o = []
			for j in range(4):
				corner = corners[j]
				o.append(corner[1] - m * corner[0] - c)
			intercept = False
			if (o[0]>0 and o[1]>0 and o[2]>0 and o[3]>0) or (o[0]<0 or o[1]<0 or o[2]<0 or o[3]>0):
				continue
			else:
				print('Player in between', x1, y1, x2, y2)
				# exit(1)
				return False
		return True
	def has_ball(self, player, ball):
		return distance(player, ball) <= 1

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
					# for i in range(TEAM_SIZE):
					# 	b1, b2 = team_opp[i]
					# 	epsilon = 1
					# 	print('Oppponent', (y2-y1) * (b1-x1), (b2-y1) * (x2-x1))
					# 	if (y2-y1) * (b1-x1) <= (b2-y1) * (x2-x1) + epsilon and (b2-y1) * (x2-x1) <= (y2-y1) * (b1-x1) + epsilon:
					# 		# exit(1)
					if self.isfree(x1, y1, x2, y2, team_own, team_opp) == False:
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

		if distance(team_own[pos], (WIDTH, HEIGHT/2)) <= 100:
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
			# print('passto', passto)
			if self.isfree(team_own[pos][0], team_own[pos][1], passto[0], passto[1], team_own, team_opp) == False:
				return team_own[pos]
			ball[0] = passto[0]
			ball[1] = passto[1]
		return team_own[pos]

class UtilityBased(Behaviour):
	def __init__(self):
		super().__init__()
	
	def distance_to_goal(self, player, goal=(WIDTH, HEIGHT/2)):
		return distance(player, goal)
	
	def opponent_player_cost(self, player, team_opp):
		score = 0
		for i in range(TEAM_SIZE):
			opp = team_opp[i]
			score = score + distance(player, opp)
		return score
	
	def distance_from_ball(self, player, ball):
		return distance(player, ball)

	def next(self, pos, team_own, team_opp, ball):
		if self.has_ball(team_own[pos], ball) == False:
			return team_own[pos]

		if ((self.distance_to_goal(team_own[pos]) <= 50.0) and (self.isfree(team_own[pos][0], team_own[pos][1], WIDTH, HEIGHT/2, team_own, team_opp))):
			ball[0] = WIDTH
			ball[1] = HEIGHT/2
			print('Shooting', self.distance_to_goal(team_own[pos], ball) <= 50, ((self.distance_to_goal(team_own[pos], ball) <= 50.0) and (self.isfree(team_own[pos][0], team_own[pos][1], WIDTH, HEIGHT/2, team_own, team_opp))))
			return team_own[pos]
		l1 = 0.5
		l2 = 1
		l3 = 0.05

		mn_score = -1
		mn_pos = -1
		for i in range(TEAM_SIZE):
			if i == pos:
				continue
			current = team_own[i]
			score = l1*self.distance_to_goal(current) + l2*self.distance_from_ball(current, ball) + l3*self.opponent_player_cost(current, team_opp)
			# print(l1*self.distance_to_goal(current), l2*self.distance_from_ball(current, ball), l3*self.opponent_player_cost(current, team_opp))
			if mn_score == -1 or score < mn_score and self.isfree(team_own[pos][0], team_own[pos][1], current[0], current[1], team_own, team_opp):
				mn_score = score
				mn_pos = i

		if mn_pos == pos:
			exit(1)
			if team_own[pos][0] == WIDTH:
				return team_own[pos][0]-50, team_own[pos]
			if self.isfree(team_own[pos][0], team_own[pos][1], team_own[pos][0]+1, team_own[pos][1], team_own, team_opp):
				return team_own[pos][0]+1, team_own[pos][1]
			if team_own[pos][1] == HEIGHT:
				return team_own[pos][0], team_own[pos][1]-50
			if self.isfree(team_own[pos][0], team_own[pos][1], team_own[pos][0], team_own[pos][1]+1, team_own, team_opp):
				return team_own[pos][0], team_own[pos][1]+1
			return team_own[pos][0]+1, team_own[pos][1]
		else:
			# passing ball to mn_pos
			passto = team_own[mn_pos]
			print('passed ball at', ball, 'to', passto)
			ball[0] = passto[0]
			ball[1] = passto[1]
			print('updated ball', ball)
			# exit(3)
			return team_own[pos]