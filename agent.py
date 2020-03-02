# Agent Object
# Has the followng properties:
#
# self.StartPos == starting position of agent
#	-2, 0, or 2
#
# self.Direction == how do they define forward
#	1 -> move right on number line
#      -1 -> move left on number line
#
# self.History == list of their movements
#	In GENERIC form (always starts with 1)
#
# self.ProbHappen == total probability this agent follows this path


class Agent:

	def __init__(self, start_pos, direction, history, phappen):
		self.StartPos = start_pos
		self.Direction = direction
		self.History = history
		self.ProbHappen = phappen

	def next_move(self, probForward):
		
		agents = []

		if probForward != 0:
			phappen_forward = self.ProbHappen * probForward
			history_forward = self.History.copy()
			history_forward.append(1)
			fAgent = Agent( self.StartPos, self.Direction, history_forward, phappen_forward)
			agents.append(fAgent)
			
		if probForward != 1:
			phappen_backward = self.ProbHappen * (1 - probForward)
			history_backward = self.History.copy()
			history_backward.append(-1)
			bAgent = Agent(self.StartPos, self.Direction, history_backward, phappen_backward)
			agents.append(bAgent)
		
		return agents	


	def __str__(self):
		return ("Starting: " + str(self.StartPos) + ", Path: " + str(self.History) + ", Direction: " + str(self.Direction) + ", Probability: " + str(self.ProbHappen))	

