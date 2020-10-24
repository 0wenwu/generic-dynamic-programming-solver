"""
knapsack.py

This demos how to solve the knapsack problem with the generic dynmaic programming solver.
The problem is to put as highest valued items to a knapsack as possible, with a constraint
of the weight capacity of the knapsack.
"""
import numpy as np
import hashlib

class KnapsackGame(object):

    """
    Define the game object for the knapsack problem.
    Every game object should implement the reset(), hash(), actionDomain(), and step() 
    method, as well as oraganise its internal state as the state object.
    """
    
    def __init__(self):
        self.capacity = None    # remaining capacity in the knapsack
        self.weights = None     # an array of weights of the N items
        self.values = None      # an array of values of the N items
        self.N = None           # number of items

    def reset(self, capacity, items, weights, values):

        """
        Reset the game to it's initial state, with the atrributes specific to the game. 
        Take the knapsack problem as an examples:
        
        capacity:   remaining capacity in the knapsack
        items:      an array storing the number of each item
        weights:    an array storing the weight of each item
        values:     an array storing the value of each item
        
        return:     an initial state object, needs not care its implementation
        """
        
        self.capacity = capacity
        self.weights = weights
        self.values = values
        self.N = len(items)
        state = np.zeros(self.N + 1)
        state[ :self.N] = items  # items available
        state[-1] = capacity
        return state


    def hash(self, state):

        """
        For checking overlapping subproblems, gives an unique hash value of a game state.

        state:      a state of the knapsack subproblem
        return:     an unique hash value for the game state
        """

        return hashlib.sha1(state).hexdigest()


    def actionDomain(self, state):

        """
        Given a game state, specify its allowed actions.

        state:      a state of the knapsack subproblem
        return:     an array of item number allowed to put into the knapsack
        """

        capacityCond = (self.weights <= state[-1])  # put only what allowed in capacity 
        availableCond = (state[ :self.N] > 0)       # put only what still available
        return np.where(capacityCond & availableCond)[0]


    def step(self, state, action):

        """
        Given a game state, take a step forward with the specified action.

        state:      the current state of the knapsack subproblem
        action:     the item number to put into the knapsack.
        return:     the next state after taking the action, assosiated with the reward.
        """

        state = state.copy()
        state[action] = state[action] - 1               # deduct the items availability
        state[-1] = state[-1] - self.weights[action]    # deduct the knapsack capacity
        return state, self.values[action]               # value increased in the knapsack


if __name__ == '__main__':       

    from dpsolver import DeterministicSolver

    """
    An example of 3 item types:
    the 1st item has weight 6 and value 12, availability is 2
    the 2nd item has weight 4 and value 11, availability is 3
    the 3rd item has weight 2.5 and value 7, availability is 1
    """
    items = np.array([2, 3, 1])
    weights = np.array([6, 4, 2.5])
    values = np.array([12, 11.5, 7])
    
    game = KnapsackGame()               # init the game object
    solver = DeterministicSolver(game)  # init the solver with the knapsack game
    
    state = game.reset(10, items, weights, values)  # reset the game to the initial state
    result = solver.solve(state)                    # solve from the initial state
    print('The max utility is %f' % result[1])
    print('The policy is:')
    print(list(solver.cache.values()))
