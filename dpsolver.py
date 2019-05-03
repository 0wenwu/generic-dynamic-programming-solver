"""
dpsolver.py
"""
import numpy as np

class DeterministicSolver(object):

    def __init__(self, game):
        self.cache = {}
        self.game = game
        self.counter = 0
        self.cachedCounter = 0

    def solve(self, state):
        self.counter += 1
        stateKey = self.game.hash(state)
        if stateKey in self.cache:
            return self.cache[stateKey]
        
        self.cachedCounter += 1
        actionSet = self.game.actionDomain(state)
        if len(actionSet) == 0: # terminal
            return 0, None

        maxValue = -99999
        optimal = None
        for action in actionSet:
            nextState, reward = self.game.step(state, action)
            utility, terminal = self.solve(nextState)
            total = reward + utility
            if utility > maxValue:
                maxValue = total
                optimal = action

        self.cache[stateKey] = maxValue, optimal
        return maxValue, optimal
    
    
class StochasticSolver(object):

    def __init__(self, game):
        self.cache = {}
        self.game = game
        self.counter = 0
        self.cachedCounter = 0

    def solve(self, state):
        self.counter += 1
        stateKey = self.game.hash(state)
        if stateKey in self.cache:
            return self.cache[stateKey]
        
        self.cachedCounter += 1
        actionSet = self.game.actionDomain(state)
        if len(actionSet) == 0: # terminal
            return 0, None

        maxValue = -99999
        optimal = None
        for action in actionSet:
            nextstates, probs, rewards = self.game.step(state, action)
            values = np.array(
                    [self.solve(nextstate)[0] for nextstate in nextstates])
            expected = np.sum(probs * (values + rewards))
            
            if expected > maxValue:
                maxValue = expected
                optimal = action

        self.cache[stateKey] = maxValue, optimal
        return maxValue, optimal