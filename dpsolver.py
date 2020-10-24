"""
dpsolver.py
"""
import numpy as np

class DeterministicSolver(object):

    """
    The generic solver for deterministic dynamic programming problem.
    """
    
    def __init__(self, game):
        """
        Constructor
        
        game: the game object modelling the problem to be solved.
        """
        self.cache = {}         # for checking overlapping subproblems
        self.game = game        # solve one game for each solver
        self.counter = 0        # records the complexity without cache
        self.cachedCounter = 0  # records the complexity with cache

    def solve(self, state):
        """
        Solves the DP problem by recursively calls to solve the smaller problems.
        
        state: feed in the initial state of the game
        return: the accumulated utility and the optimal action
        """
        self.counter += 1                       # record how many subproblems
        stateKey = self.game.hash(state)        # hash the state to check overlapping
        if stateKey in self.cache:              # if subproblem is overlapped
            return self.cache[stateKey][1:]     # return solved subproblem immediately
        
        self.cachedCounter += 1     # record how many non-overlapping subproblems
        actionSet = self.game.actionDomain(state)
        if len(actionSet) == 0:     # terminal condition
            return None, 0          # return recursive call at terminal

        maxUtility = -99999     # maximum utility (with the optimal path)
        optimal = None          # optimal action
        for action in actionSet:
            nextState, reward = self.game.step(state, action)
            terminal, utility = self.solve(nextState)   # solve the small subproblem
            total = reward + utility
            if utility > maxUtility:    # test which action is the best
                maxUtility = total
                optimal = action

        self.cache[stateKey] = state, optimal, maxUtility   # cache the solution
        return optimal, maxUtility  # return optimal action and max utility
    
    
class StochasticSolver(object):

    """
    The generic solver for stochastic dynamic programming problem.
    """

    def __init__(self, game):
        self.cache = {}         # for checking overlapping subproblems
        self.game = game        # solve one game for each solver
        self.counter = 0        # records the complexity without cache
        self.cachedCounter = 0  # records the complexity with cache

    def solve(self, state):
        
        """
        Solves the DP problem by recursively calls to solve the smaller problems.
        
        state: feed in the initial state of the game
        return: the accumulated expected utility and the optimal action
        """

        self.counter += 1                   # record how many subproblems
        stateKey = self.game.hash(state)    # hash the state to check overlapping
        if stateKey in self.cache:          # if subproblem is overlapped
            return self.cache[stateKey][1:]     # return solved subproblem immediately
        
        self.cachedCounter += 1     # record how many non-overlapping subproblems
        actionSet = self.game.actionDomain(state)
        if len(actionSet) == 0:     # terminal condition
            return None, 0          # return recursive call at terminal

        maxUtility = -99999         # maximum utility (with the optimal path)
        optimal = None              # optimal action
        for action in actionSet:
            # step forward and output the state objects, probabilities and rewards for 
            # all possibile next states
            nextStates, probs, rewards = self.game.step(state, action)
            utilities = np.array([self.solve(nextstate)[1] for nextstate in nextStates])
            expectedValue = np.sum(probs * (utilities + rewards))
            
            if expectedValue > maxUtility:
                maxUtility = expectedValue
                optimal = action

        self.cache[stateKey] = state, optimal, maxUtility
        return optimal, maxUtility 