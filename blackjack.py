"""
blackjack.py
"""
import numpy as np
import hashlib

class BlackjackGame(object):

    def __init__(self):
        pass
    
    
    def reset(self, usableace, playersum, dealercard):
        state = np.zeros(7)
        state[1] = playersum
        state[2] = usableace
        state[3] = 11 if dealercard == 1 else dealercard
        state[4] = int(dealercard == 1)
        return state


    def hash(self, state):
        return hashlib.sha1(state).hexdigest()


    def actionDomain(self, state):
        if state[0] == 0: # player turns
            return [0, 1] # player hit or stick
        
        elif state[0] == 1: #dealer turns
            if state[3] < 17: 
                return [2] # dealer must hit when sum < 17
            elif state[3] < state[1]: 
                return [2] # dealer must hit when sum smaller than player
            else:
                return [3] # dealer stick
        
        return [] # game end
            

    def step(self, state, action):
        newstates = np.tile(state, (10, 1))
        cards = np.arange(0, 10)
        cards[0:2] += 10
        probs = np.zeros(10) 
        probs[0] = 4. * 4. / 52. # 10
        probs[1:10] = 4. / 52. # Ace and 2-9
        rewards = np.zeros(10)
        
        if action == 0: # player hit
            newstates[:, 1] += cards
            newstates[1, 2] += 1 # add 1 usable ace            
            mask_bust = (newstates[:, 1] > 21)
            mask_usableace = (newstates[:, 2] > 0)
            newstates[mask_bust & mask_usableace, 2] -= 1 # use up 1 ace
            newstates[mask_bust & mask_usableace, 1] -= 10 # sum reduce by 10
            mask_bust = (newstates[:, 1] > 21)
            newstates[mask_bust, 0] = 2 # game end for bust
            rewards[mask_bust] = -1 # player loss
            return newstates, probs, rewards
        
        elif action == 1: # player stick
            newstate = state.copy()
            newstate[0] = 1 # signal dealer turns
            return np.array([newstate]), 1, 0
        
        elif action == 2: # dealer hit
            newstates[:, 3] += cards
            newstates[1, 4] += 1 # add 1 usable ace            
            mask_bust = (newstates[:, 3] > 21)
            mask_usableace = (newstates[:, 4] > 0)            
            newstates[mask_bust & mask_usableace, 4] -= 1 # use up 1 ace
            newstates[mask_bust & mask_usableace, 3] -= 10 # sum reduce by 10
            mask_bust = (newstates[:, 3] > 21)
            newstates[mask_bust, 0] = 2 # game end for bust
            rewards[mask_bust] = 1 # player win
            return newstates, probs, rewards
        
        # dealer stick
        newstate = state.copy()
        newstate[0] = 2 # signal game end
        reward = np.sign(newstate[1] - newstate[3]) 
        return np.array([newstate]), 1, reward # 1 win, -1 loss, 0 draw
    
