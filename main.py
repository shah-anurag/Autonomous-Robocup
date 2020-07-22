from tkinter import Tk, Canvas
import time

import agent
import behaviour
import random
import multiprocessing
import field
import config_values

TEAM_SIZE = config_values.TEAM_SIZE
LENGTH = config_values.LENGTH
WIDTH = config_values.WIDTH

canvas = None
root = None

def initialize():
	teamA = []
	teamB = []
	pA = []
	pB = []

	for i in range(0, TEAM_SIZE):
		b = behaviour.Behaviour()
		
		agentA = agent.Agent((i+1), b, int(i * LENGTH / TEAM_SIZE), int(random.uniform(0, WIDTH)))
		agentB = agent.Agent(-(i+1), b, int(LENGTH - (i * LENGTH / TEAM_SIZE)), int(random.uniform(0, WIDTH)))
		
		p1A = multiprocessing.Process(target = agentA.run)
		p1B = multiprocessing.Process(target = agentB.run)
		
		teamA.append(agentA)
		teamB.append(agentB)

		p1A.start()
		p1B.start()

		# p1A.join()
		# p1B.join()

		pA.append(p1A)
		pB.append(p1B)
		
	#field_ = field.Field()
	#field_p = multiprocessing.Process(target = field_.main)
	#field_p.start()
	print('HHM')
	return teamA, teamB, pA, pB

def stop(pA, pB):
	for p in pA:
		p.close()
	for p in pB:
		p.close()
	return

def main():
	teamA, teamB, pA, pB = initialize()
	ball = [LENGTH/2, WIDTH/2]
	while True:
		team_red = [agent.get_coordinates() for agent in teamA]
		team_blue = [agent.get_coordinates() for agent in teamB]
		print(team_red)
		print(team_blue)
		field.update_positions(team_red, team_blue, ball, canvas)
		root.update()
		time.sleep(5)
	print('YOYOYO')
	# stop(pA, pB)

root = Tk()
root.geometry(field.windowDims())
root.title("Robocup Simulation")
canvas = Canvas()
field.drawField(canvas)
field.initialize_players(canvas)
main()
root.mainloop()
print("Window closed")
#main()
