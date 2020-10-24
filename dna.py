"""
dna.py

This demos how to solve the DNA alignment problem with the generic DP solver.
The problem is to maximize the total score for aligning a pair of DNA sequences, reward a 
score if for a local match, deduct for a substitution, and deduct another score for an 
insert or a deletion.
"""

class DnaAlignGame(object):

    """
    Define the game object for the DNA alignment problem. 
    Every game object should implement the reset(), hash(), actionDomain(), and step() 
    method, as well as oraganise its internal state as the state object.
    """

    def __init__(self):
        self.reward_match = 5       # the reward for a local match
        self.penalty_subst = -2     # the penalty for a local substitution
        self.penalty_insdel = -6    # the penalty for a local insert or deletion
        
    def reset(self, x, y):

        """
        Reset the game to it's initial state, with the atrributes specific to the game. 
        Take the DNA alignment problem as an examples:
        
        x:  the 1st DNA sequence
        y:  the 2nd DNA sequence
        
        return:     an initial state object, needs not care its implementation
        """

        state = (x, y)
        return state


    def hash(self, state):
        
        """
        For checking overlapping subproblems, gives an unique hash value of a game state.

        state:      a state of the DNA alginment subproblem
        return:     an unique hash value for the game state
        """

        x, y = state
        return hash(x + ',' + y)


    def actionDomain(self, state):

        """
        Given a game state, specify its allowed actions.

        state:      a state of the DNA sequences pair
        return:     an array of available actions:
                    0 - use both X & Y, either match or substitute
                    1 - use X only, delete X or insert Y
                    2 - use Y only, delete Y or insert X
        """


        x, y = state
        if len(x) > 0 and len(y) > 0: 
            return [0, 1, 2]
        elif len(x) > 0:
            return [1]
        elif len(y) > 0:
            return [2]

        return []
            

    def step(self, state, action):
        
        """
        Given a game state, take a step forward with the specified action.

        state:      the current state of the DNA sequences pair
        action:     0 - use both X & Y, either match or substitute
                    1 - use X only, delete X or insert Y
                    2 - use Y only, delete Y or insert X
        
        return:     the next state after taking the action, assosiated with the reward.
        """

        x, y = state
        if action == 0:  # use both
            if x[0] == y[0]:
                reward = self.reward_match
            else:
                reward = self.penalty_subst
            
            x = x[1:]
            y = y[1:]
        
        elif action == 1: # use x only
            reward = self.penalty_insdel
            x = x[1:]
        
        else: # use y only 
            reward = self.penalty_insdel
            y = y[1:]
        
        state = (x, y)
        return state, reward # value added

    
if __name__ == '__main__':       

    from dpsolver import DeterministicSolver

    """
    An example of aligning two DNA sequences:
    """
    x = 'TTCATA'
    y = 'TGCTCGTA'
    
    game = DnaAlignGame()               # init the game object
    solver = DeterministicSolver(game)  # init the solver with the knapsack game
    
    state = game.reset(x, y)            # reset the game to the initial state
    result = solver.solve(state)        # solve from the initial state
    print('The max utility is %f' % result[1])
    print('The policy is:')
    print(list(solver.cache.values()))
