"""
dna.py
"""
class DnaAlignGame(object):

    def __init__(self):
        self.reward_match = 5
        self.penalty_subst = -2
        self.penalty_insdel = -6
        
    def reset(self, x, y):
        state = (x, y)
        return state

    def hash(self, state):
        x, y = state
        return hash(x + ',' + y)

    def actionDomain(self, state):
        x, y = state
        if len(x) > 0 and len(y) > 0: 
            return [0, 1, 2]
        elif len(x) > 0:
            return [1]
        elif len(y) > 0:
            return [2]

        return []
            

    def step(self, state, action):
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