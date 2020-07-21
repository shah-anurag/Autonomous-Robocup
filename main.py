import agent
import behaviour
import random
import multiprocessing
import field

TEAM_SIZE = 2
LENGTH = 750
WIDTH = 1200

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

	field_ = field.Field()
	field_p = multiprocessing.Process(target = field_.main)
	field_p.start()

	return teamA, teamB, pA, pB, field_

def stop(pA, pB):
	for p in pA:
		p.stop()
	for p in pB:
		p.stop()
	return

def main():
	teamA, teamB, pA, pB, field_ = initialize()
	ball = [LENGTH/2, WIDTH/2]
	while True:
		team_red = [agent.get_coordinates() for agent in teamA]
		team_blue = [agent.get_coordinates() for agent in teamB]
		field_.update_positions(team_red, team_blue, ball)
	print('YOYOYO')
	# stop(pA, pB)

main()