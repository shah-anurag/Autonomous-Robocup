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
			eps = 100
			if (distance((x1,y1), opp) > distance((x1,y1), (x2,y2))) + eps or (distance((x2,y2), opp) > distance((x1,y1), (x2,y2))) + eps:
				continue
			step = 200
			corners = [(opp[0], opp[1]), (opp[0]+step, opp[1]+step), (opp[0]+step, opp[1]-step), (opp[0]-step, opp[1]+step), (opp[0]-step, opp[1]-step)]
			o = []
			for j in range(len(corners)):
				corner = corners[j]
				o.append(corner[1] - m * corner[0] - c)
			if (o[0]>0 and o[1]>0 and o[2]>0 and o[3]>0) or (o[0]<0 or o[1]<0 or o[2]<0 or o[3]<0):
				continue
			else:
				# print('Player in between', x1, y1, x2, y2)
				return False
		return True
	def has_ball(self, player, ball):
		return distance(player, ball) <= 2

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
					if self.isfree(x1, y1, x2, y2, team_own, team_opp) == False:
						return team_own[pos]
					ball[0] = x2+1		# Pass the ball
					ball[1] = y2
					return team_own[pos]
			else :	# Current player doesnot have the ball but is nearest to the ball
				x1,y1 = team_own[pos]
				if ball[0] > x1:
					x1 = x1 + 1
				elif ball[0] < x1:
					x1 = x1 - 1
				if ball[1] > y1:
					y1 = y1 + 1
				elif ball[1] < y1:
					y1 = y1 - 1
				return x1, y1
		else :	# Current player is not nearest to the ball
			if distance_to_ball <= 1: # If player at pos_min has the ball
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
			score = score + distance(player, opp)#**2
		return score
	
	def distance_from_ball(self, player, ball):
		return distance(player, ball)
		
	def move_toward_ball(self, player, ball):
		mag = ((ball[0]-player[0])**2 + (ball[1]-player[1])**2)**0.5
		direction = ((ball[0]-player[0])/mag, (ball[1]-player[1])/mag)
		dx, dy = direction[0]*TIMESTEP*PASSIVE_SPEED, direction[1]*TIMESTEP*PASSIVE_SPEED
		new_x, new_y = player[0]+dx, player[1]+dy
		return new_x, new_y
		
	def move_toward_goal(self, player, goal=(WIDTH, HEIGHT/2)):
		mag = ((goal[0]-player[0])**2 + (goal[1]-player[1])**2)**0.5
		direction = ((goal[0]-player[0])/mag, (goal[1]-player[1])/mag)
		dx, dy = direction[0]*TIMESTEP*ACTIVE_SPEED, direction[1]*TIMESTEP*ACTIVE_SPEED
		new_x, new_y = player[0]+dx, player[1]+dy
		return new_x, new_y
		
	def center_of_cluster(self, pos, team_own):
		player = team_own[pos]
		others = team_own[:pos]+team_own[pos+1:]
		so_oth = sorted(others, key=lambda x:distance(x, player))
		return so_oth[0]
	
	def slow_move_and_decluster(self, pos, team_own, ball, goal=(WIDTH, HEIGHT/2)):
		decluster_fac = 0.5
		move_ahead_fac = 0.8
		ball_fac = 0.1
		
		norm = decluster_fac+move_ahead_fac+ball_fac
		decluster_fac /= norm
		move_ahead_fac /= norm
		ball_fac /= norm
		player = team_own[pos]
		
		mag = ((goal[0]-player[0])**2 + (goal[1]-player[1])**2)**0.5
		direction = ((goal[0]-player[0])/mag, (goal[1]-player[1])/mag)
		dx1, dy1 = direction[0]*TIMESTEP*PASSIVE_SPEED, direction[1]*TIMESTEP*PASSIVE_SPEED
		
		centroid = self.center_of_cluster(pos, team_own)
		decluster_thresh = 200
		if(distance(player, centroid)>decluster_thresh):
			dx2, dy2 = 0, 0
		else:
			mag = ((centroid[0]-player[0])**2 + (centroid[1]-player[1])**2)**0.5
			direction = ((centroid[0]-player[0])/mag, (centroid[1]-player[1])/mag)
			dx2, dy2 = direction[0]*TIMESTEP*PASSIVE_SPEED, direction[1]*TIMESTEP*PASSIVE_SPEED
		
		mag = ((ball[0]-player[0])**2 + (ball[1]-player[1])**2)**0.5
		direction = ((ball[0]-player[0])/mag, (ball[1]-player[1])/mag)
		dx3, dy3 = direction[0]*TIMESTEP*PASSIVE_SPEED, direction[1]*TIMESTEP*PASSIVE_SPEED
		
		new_x = player[0]+move_ahead_fac*dx1-decluster_fac*dx2+ball_fac*dx3
		new_y = player[1]+move_ahead_fac*dy1-decluster_fac*dy2+ball_fac*dy3
		return new_x, new_y

	def next(self, pos, team_own, team_opp, ball):
		# if ball is at goal, then stop
		if(ball[0]==WIDTH and ball[1]==HEIGHT/2):
			return team_own[pos]
		# if not have ball, then move toward the ball slowly
		if self.has_ball(team_own[pos], ball) == False:
			#new_pos = self.move_toward_ball(team_own[pos], ball)
			if(ball[0]==WIDTH/2 and ball[1]==HEIGHT/2):
				new_pos = self.move_toward_ball(team_own[pos], ball)
			else:
				new_pos = self.slow_move_and_decluster(pos, team_own, ball)
			return new_pos
		#return team_own[pos]	
		# if close to goal and nobody in between then shoot
		if ((self.distance_to_goal(team_own[pos]) <= 50.0) and (self.isfree(team_own[pos][0], team_own[pos][1], WIDTH, HEIGHT/2, team_own, team_opp))):
			ball[0] = WIDTH
			ball[1] = HEIGHT/2
			print('Goal Done, stopping players')
			#print('Shooting', self.distance_to_goal(team_own[pos], ball) <= 50, ((self.distance_to_goal(team_own[pos], ball) <= 50.0) and (self.isfree(team_own[pos][0], team_own[pos][1], WIDTH, HEIGHT/2, team_own, team_opp))))
			return team_own[pos]
		
		# choose whether to move forward or pass
		l1 = -0.5 # weight for candidate close to goal, less is better
		l2 = -0.5 # weight for candidate close to ball, less is better
		l3 = 0.2 # weight for candidate close to opponents, more is better

		max_score = -100000
		max_pos = -1
		for i in range(TEAM_SIZE):
			# if i == pos:
			#	continue
			current = team_own[i]
			# check if way is clear, if not clear then ignore current
			if (not self.isfree(team_own[pos][0], team_own[pos][1], current[0], current[1], team_own, team_opp)):
				continue
			score = l1*self.distance_to_goal(current) + l2*self.distance_from_ball(current, ball) + l3*self.opponent_player_cost(current, team_opp)
			# print(l1*self.distance_to_goal(current), l2*self.distance_from_ball(current, ball), l3*self.opponent_player_cost(current, team_opp))
			if(score>max_score):
				max_score = score
				max_pos = i
		
		if max_pos==-1:
			max_pos = pos
		
		if max_pos==pos:
			new_pos = self.move_toward_goal(team_own[pos])
			ball[0] = new_pos[0]
			ball[1] = new_pos[1]
			#print('updated ball', ball)
			return new_pos
			
		else:
			# passing ball to mn_pos
			passto = team_own[max_pos]
			print('passed ball at', ball, 'to', passto)
			ball[0] = passto[0]
			ball[1] = passto[1]
			#print('updated ball', ball)
			# exit(3)
			return team_own[pos]
			
class Defenders(Behaviour):
	def __init__(self):
		super().__init__()

	def var_speed(self, pos, team_own, ball):
		d = self.distance(team_own[pos], ball)
		dmax = 0
		for i in range(TEAM_SIZE):
			dmax = max(dmax, distance(team_own[i], ball))
		if d*3 <= dmax:
			return 5
		if d*3 <= dmax*2:
			return 2.5
		return 1
	
	def interfere_point(self, ball, goal=(WIDTH, HEIGHT/2)):
		target_x, target_y = (ball[0]+goal[0])/2, (ball[1]+goal[1])/2
		return target_x, target_y
	
	def center_of_cluster(self, pos, team_own):
		player = team_own[pos]
		others = team_own[:pos]+team_own[pos+1:]
		so_oth = sorted(others, key=lambda x:distance(x, player))
		return so_oth[0]
	
	def move_between_ball_and_goal(self, player, ball,  goal=(WIDTH, HEIGHT/2)):
		target = self.interfere_point(ball)
		mag = ((target[0]-player[0])**2 + (target[1]-player[1])**2)**0.5
		direction = ((target[0]-player[0])/mag, (target[1]-player[1])/mag)
		dx, dy = direction[0]*TIMESTEP*PASSIVE_SPEED, direction[1]*TIMESTEP*PASSIVE_SPEED
		new_x, new_y = player[0]+dx, player[1]+dy
		return new_x, new_y
		
	def interfere_and_decluster(self, pos, team_own, ball, goal=(WIDTH, HEIGHT/2)):
		decluster_fac = 0.8
		move_ahead_fac = 0.5
		
		norm = decluster_fac+move_ahead_fac
		decluster_fac /= norm
		move_ahead_fac /= norm
		player = team_own[pos]
		
		target = self.interfere_point(ball)
		mag = ((target[0]-player[0])**2 + (target[1]-player[1])**2)**0.5
		direction = ((target[0]-player[0])/mag, (target[1]-player[1])/mag)
		dx1, dy1 = direction[0]*TIMESTEP*DEFEND_SPEED, direction[1]*TIMESTEP*DEFEND_SPEED
		
		centroid = self.center_of_cluster(pos, team_own)
		decluster_thresh = 300
		if(distance(player, centroid)>decluster_thresh):
			dx2, dy2 = 0, 0
		else:
			mag = ((centroid[0]-player[0])**2 + (centroid[1]-player[1])**2)**0.5
			direction = ((centroid[0]-player[0])/mag, (centroid[1]-player[1])/mag)
			dx2, dy2 = direction[0]*TIMESTEP*PASSIVE_SPEED, direction[1]*TIMESTEP*PASSIVE_SPEED
		
		
		new_x = player[0]+(move_ahead_fac*dx1-decluster_fac*dx2)*self.var_speed(pos, team_own, ball)
		new_y = player[1]+(move_ahead_fac*dy1-decluster_fac*dy2)*self.var_speed(pos, team_own, ball)
		return new_x, new_y

	
	def next(self, pos, team_own, team_opp, ball):
		if(ball[0]==WIDTH and ball[1]==HEIGHT/2):
			return team_own[pos]
		new_pos = self.interfere_and_decluster(pos, team_own, ball)
		return new_pos