from tkinter import Tk, Canvas
import time
import agent
import behaviour
import random
import field
from config_values import *

canvas = None
root = None

def initialize():
	teamA = []
	teamB = []
	pA = []
	pB = []

	for i in range(0, TEAM_SIZE):
		bA = behaviour.UtilityBased()
		bB = behaviour.Defenders()
		
		agentA = None
		if i == 0:
			agentA = agent.Agent(1, bA, WIDTH//2, HEIGHT//2)
		else:
			agentA = agent.Agent((i+1), bA, int(random.uniform(0, WIDTH//2)), int(random.uniform(0, HEIGHT)))
		agentB = agent.Agent(-(i+1), bB, int(random.uniform(WIDTH//2, WIDTH)), int(random.uniform(0, HEIGHT)))

		teamA.append(agentA)
		teamB.append(agentB)

	return teamA, teamB

def stop(pA, pB):
	for p in pA:
		p.close()
	for p in pB:
		p.close()
	return

def main():
	teamA, teamB = initialize()
	ball = [WIDTH//2, HEIGHT//2]
	while True:
		team_red = [agent.get_coordinates() for agent in teamA]
		team_blue = [agent.get_coordinates() for agent in teamB]

		for agent in teamA:
			agent.update(team_own=team_red, team_opp=team_blue, ball=ball)
		for agent in teamB:
			agent.update(team_own=team_blue, team_opp=team_red, ball=ball)

		team_red = [agent.get_coordinates() for agent in teamA]
		team_blue = [agent.get_coordinates() for agent in teamB]

		field.update_positions(team_red, team_blue, ball, canvas)
		root.update()
		time.sleep(TIMESTEP)

root = Tk()
root.geometry(field.windowDims())
root.title("Robocup Simulation")
canvas = Canvas()
field.drawField(canvas)
field.initialize_players(canvas)
main()
print("Window closed")