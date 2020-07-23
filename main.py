from tkinter import Tk, Canvas
import time

import agent
import behaviour
import random
import multiprocessing
import field
import config_values

TEAM_SIZE = config_values.TEAM_SIZE
HEIGHT = config_values.HEIGHT
WIDTH = config_values.WIDTH

canvas = None
root = None

def initialize():
	teamA = []
	teamB = []
	pA = []
	pB = []

	for i in range(0, TEAM_SIZE):

		bA = behaviour.RuleBased()
		bB = behaviour.Random()
		
		agentA = None
		if i == 0:
			agentA = agent.Agent(1, bA, WIDTH//2, HEIGHT//2)
		else:
			agentA = agent.Agent((i+1), bA, int(random.uniform(0, WIDTH//2)), int(random.uniform(0, HEIGHT)))
		agentB = agent.Agent(-(i+1), bB, int(random.uniform(WIDTH//2, WIDTH)), int(random.uniform(0, HEIGHT)))
		
		# p1A = multiprocessing.Process(target = agentA.run)
		# p1B = multiprocessing.Process(target = agentB.run)
		
		teamA.append(agentA)
		teamB.append(agentB)

		# p1A.start()
		# p1B.start()

		# p1A.join()
		# p1B.join()

		# pA.append(p1A)
		# pB.append(p1B)
		
	#field_ = field.Field()
	#field_p = multiprocessing.Process(target = field_.main)
	#field_p.start()
	# print('HHM')
	return teamA, teamB
	# return teamA, teamB, pA, pB

def stop(pA, pB):
	for p in pA:
		p.close()
	for p in pB:
		p.close()
	return

def main():
	# teamA, teamB, pA, pB = initialize()
	teamA, teamB = initialize()
	ball = [WIDTH//2, HEIGHT//2]
	while True:
		
		team_red = [agent.get_coordinates() for agent in teamA]
		team_blue = [agent.get_coordinates() for agent in teamB]
		# print(team_red)
		# print(team_blue)

		for agent in teamA:
			agent.update(team_own=team_red, team_opp=team_blue, ball=ball)
		for agent in teamB:
			agent.update(team_own=team_blue, team_opp=team_red, ball=ball)

		team_red = [agent.get_coordinates() for agent in teamA]
		team_blue = [agent.get_coordinates() for agent in teamB]

		field.update_positions(team_red, team_blue, ball, canvas)
		root.update()
		# time.sleep(0.02)
	# print('YOYOYO')
	# stop(pA, pB)

root = Tk()
root.geometry(field.windowDims())
root.title("Robocup Simulation")
canvas = Canvas()
field.drawField(canvas)
field.initialize_players(canvas)
main()
#root.mainloop()
print("Window closed")
#main()
