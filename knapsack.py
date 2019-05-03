"""
knapsack.py
"""
import numpy as np
import hashlib

class KnapsackGame(object):

    def __init__(self):
        self.capacity = None
        self.weights = None
        self.values = None
        self.N = None

    def reset(self, capacity, items, weights, values):
        self.capacity = capacity
        self.weights = weights
        self.values = values
        self.N = len(items)
        state = np.zeros(self.N + 1)
        state[ :self.N] = items  # items available
        state[-1] = capacity
        return state

    def hash(self, state):
        return hashlib.sha1(state).hexdigest()

    def actionDomain(self, state):
        capacityCond = (self.weights <= state[-1])
        availableCond = (state[ :self.N] > 0)
        return np.where(capacityCond & availableCond)[0]

    def step(self, state, action):
        state = state.copy()
        state[action] = state[action] - 1 # items available
        state[-1] = state[-1] - self.weights[action]  # capacity
        return state, self.values[action] # value added