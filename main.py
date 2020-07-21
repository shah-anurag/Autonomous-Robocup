import agent
import behaviour
import random
import multiprocessing

TEAM_SIZE = 11
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

		pA.append(p1A)
		pB.append(p1B)

	return agentA, agentB, pA, pB

def stop(pA, pB):
	for p in pA:
		p.stop()
	for p in pB:
		p.stop()
	return

def main():
	agentA, agentB, pA, pB = initialize()
	ball = [LENGTH/2, WIDTH/2]
	print('YOYOYO')
	# stop(pA, pB)

main()