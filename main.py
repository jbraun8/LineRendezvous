# Main Wrapper Script

import sys
from agent import Agent
from operator import contains
from confidence_function import conf
import itertools
from math import exp

return_smart_bool = True

def get_expectation(num_moves, params):
	# num_moves = int, how many moves to complete
	# params = list, parameters for confidence function

	# initializations
	distribution = dict()
	LB_on_Strategy = 0
	prob_no_rendezvous = 1
	
	# create initial agents
	agents_main = [Agent(0,1,[],1)]
	agents_other = []
	agents_other.append(Agent(2,1,[],0.25))
	agents_other.append(Agent(2,-1,[],0.25))
	agents_other.append(Agent(-2,1,[],0.25))
	agents_other.append(Agent(-2,-1,[],0.25))
	tracker = 1

	for i in range(num_moves + 1):
		# have every agent complete next move
		# build new collection of main and other agents from these moves
		new_agents_main = []
		new_agents_other = []
		correspondence = {}
		pRzvous = 0

		for toExamine_main in agents_main:
			# iterate through every main agent
			# initialize current position and probabilities forward and backward for other
			currentPos = sum(toExamine_main.History)
			probForward = 0
			probBackward = 0			
			flag = False

			for toExamine_other in agents_other:
				# iterate through every other agent
				# check if rendezvous occurs
				rBool = rendezvous_bool(toExamine_main, toExamine_other)
				if rBool[:2] != [True, False]:
					if rBool[1] == True:
						pRzvous += (toExamine_other.ProbHappen * toExamine_main.ProbHappen)
					else:
						if toExamine_other.StartPos == 2:
							probForward += toExamine_other.ProbHappen
						elif toExamine_other.StartPos == -2:
							probBackward += toExamine_other.ProbHappen

			# get probForward from Bayes Rule
			probForward = probForward / (probForward + probBackward)
			
			# soft max? 
			#probForward = exp(probForward) / ( exp(probForward) + exp(probBackward) )
			if i != num_moves:
				pF = conf(probForward, params)		
				if i == 0:
					pF = 1
				correspondence[str(toExamine_main.History)] = pF
				new_agents_main.extend(toExamine_main.next_move(pF))

		if i != num_moves:
			for toExamine_other in agents_other:
				pF = correspondence[str(toExamine_other.History)]
				new_agents_other.extend(toExamine_other.next_move(pF))
	
			agents_main = new_agents_main
			agents_other = new_agents_other

		distribution[i] = pRzvous
		prob_no_rendezvous -= pRzvous
		LB_on_Strategy += pRzvous * (i)
		
		if i == num_moves and return_smart_bool == True:
			print("Returning smart...")
			[LB_smart, UB_smart] = return_smart(agents_main, agents_other, num_moves, LB_on_Strategy, prob_no_rendezvous)
	
	LB = LB_on_Strategy + ((num_moves + 1) * prob_no_rendezvous)
	UB = LB_on_Strategy/(1 - prob_no_rendezvous) + 2*(num_moves) * ((prob_no_rendezvous)/(1 - prob_no_rendezvous)) 
		
	print("Lower Bound on Strategy: " + str(LB))
	print("Upper Bound on Rs: " + str(UB))
	print("Probability No Rendezvous: " + str(prob_no_rendezvous))
	print("Distribution: " + str(distribution))	

	return [distribution, LB, UB, LB_smart, UB_smart]
										
def rendezvous_bool(agentMain, agentOther):
	# Takes two agents, returns their rendezvous information
	# Returns [Bool1, Bool2, Count]
	# Bool1 = Do the two agents ever rendezvous?
	# Bool2 = Did Rendezvous occur in the last move?
	# Count = How many moves to rendezvous

	StartPosMain = agentMain.StartPos
	DirectionMain = agentMain.Direction
	history_main = agentMain.History

	StartPosOther = agentOther.StartPos
	DirectionOther = agentOther.Direction
	history_other = agentOther.History

	count = 0
	pos_main = StartPosMain
	pos_other = StartPosOther

	for index in range(len(history_main)):
		count += 1
		pos_main += DirectionMain * history_main[index]
		pos_other += DirectionOther * history_other[index]
		if pos_main == pos_other and index == len(history_main) - 1:
			return [True, True, count]
		elif pos_main == pos_other and index != len(history_main) - 1:
			return [True, False, count]

	return [False, False, 0]							

def return_smart(agentsMain, agentsOther, moves_completed, En, prob_no_rendezvous):

	
	agentsMain_return = []
	agentsOther_return = []
	
	directions = [-1,1]
	starting = [-2,2]
	probability_gain = 0

	for agentMain in agentsMain:
		[strategies, probability] = get_return_strategies(agentMain)
		history = agentMain.History
		for return_strat in strategies:
			newAgent = Agent(0, 1, history + list(return_strat), agentMain.ProbHappen * probability)
			agentsMain_return.append(newAgent)
			for direction in directions:
				for start in starting:
					agentsOther_return.append(Agent(start, direction, history + list(return_strat), 0.25 * agentMain.ProbHappen * probability)) 
	
	for agentMain_return in agentsMain_return:
		for agentOther_return in agentsOther_return:		
			rBool = rendezvous_bool(agentMain_return, agentOther_return)
			if rBool[0] == True:
				i = rBool[2]
				if i > moves_completed:
					probability_occur = agentMain_return.ProbHappen * agentOther_return.ProbHappen
					probability_gain += probability_occur
					En += i * probability_occur
	LB_on_Strategy = En
	prob_no_rendezvous -= probability_gain

	LB_smart = LB_on_Strategy + (2*(moves_completed) + 1) * prob_no_rendezvous
	UB_smart = LB_on_Strategy/(1 - prob_no_rendezvous) + 2*(moves_completed) * ((prob_no_rendezvous)/(1 - prob_no_rendezvous))

	print(En)
	print("Lower Bound (smart): " + str(LB_smart))
	print("Upper Bound (smart): " + str(UB_smart))
	print("Probability No Rendezvous (smart): " + str(prob_no_rendezvous))
	return [LB_smart, UB_smart]


def get_return_strategies(agent):
	# Return a list of all possible return strategies for an agent
 
	return_sequence = [i * -1 for i in agent.History]

	# Return every possible way with equal probability
	#strategies = list(set(itertools.permutations(return_sequence)))
	#probability = 1 / len(strategies)

	# Return the way you came or the reverse with equal probability
	strategies = [ return_sequence, list(reversed(return_sequence)) ]
	probability = 0.5

	return [strategies, probability]
		

if __name__ == "__main__":
	num_moves = int(sys.argv[1])
	params = [int(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4])]
	get_expectation(num_moves,params)
