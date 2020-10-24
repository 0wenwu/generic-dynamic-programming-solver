"""
blackjack.py

This demos how to play Blackjack with the stochastic dynamic programming solver.
In Blackjack, the player hits to collect cards until he is enough and sticks. Then it 
starts the deal turn. The player's goal is to collect cards that sum up larger than the 
dealer's sum without exceeding 21.  What complicated the game is that an Ace can be 
counted as either 1 or 11, whichever to maximize the holder's goal.
"""

import numpy as np
import hashlib

class BlackjackGame(object):

    """
    Define the game object for the Blackjack game.
    Every game object should implement the reset(), hash(), actionDomain(), and step() 
    method, as well as oraganise its internal state as the state object.
    """

    def __init__(self):
        pass
    
    
    def reset(self, usableace, playersum, dealercard):
        
        """
        Reset the game to it's initial state, with the atrributes specific to the game. 
        Take the Blackjack problem as an examples:
        
        usableace:      whether the player has an usable Ace (unconverted to 11)
        playersum:      the sum of the player's card
        dealercard:     the visible card of the dealer
        
        return:     an initial state object, needs not care its implementation
        """

        state = np.zeros(7)                                 # state[0]: whose turn
        state[1] = playersum
        state[2] = usableace
        state[3] = 11 if dealercard == 1 else dealercard    # initially count ace as 11
        state[4] = int(dealercard == 1)                     # whether dealer has an ace
        return state


    def hash(self, state):

        """
        For checking overlapping subproblems, gives an unique hash value of a game state.

        state:      a state of the Blackjack game
        return:     an unique hash value for the game state
        """

        return hashlib.sha1(state).hexdigest()


    def actionDomain(self, state):
        
        """
        Given a game state, specify its allowed actions.

        state:      a state of the Blackjack game
        return:     an array of possible actions:
                    0 - player hits
                    1 - player sticks
                    2 - dealer hits
                    3 - dealer sticks
        """

        if state[0] == 0:       # player turns
            return [0, 1]       # player hit or stick
        
        elif state[0] == 1:     #dealer turns
            if state[3] < 17: 
                return [2]      # dealer must hit when sum < 17
            elif state[3] < state[1]: 
                return [2]      # dealer must hit when sum smaller than player
            else:
                return [3]      # dealer stick
        
        return []               # game end
            

    def step(self, state, action):
        
        """
        Given a game state, take a step forward with the specified action.

        state:      the current state of the DNA sequences pair
        action:     0 - player hits
                    1 - player sticks
                    2 - dealer hits
                    3 - dealer sticks

        return:     an array of all possible next states after taking the action, 
                    together with the assosiated probabilities and rewards.
        """

        newstates = np.tile(state, (10, 1))
        cards = np.arange(0, 10)        # all possible card points
        cards[0:2] += 10
        probs = np.zeros(10)            # card points' probabilities
        probs[0] = 4. * 4. / 52.        # 10, J, Q, K
        probs[1:10] = 4. / 52.          # Ace and 2-9
        rewards = np.zeros(10)          # rewards are zeros unless end game
        
        if action == 0:                                         # player hit
            newstates[:, 1] += cards
            newstates[1, 2] += 1                                # add 1 usable ace            
            mask_bust = (newstates[:, 1] > 21)
            mask_usableace = (newstates[:, 2] > 0)
            newstates[mask_bust & mask_usableace, 2] -= 1       # use up 1 ace
            newstates[mask_bust & mask_usableace, 1] -= 10      # sum reduce by 10
            mask_bust = (newstates[:, 1] > 21)
            newstates[mask_bust, 0] = 2                         # game end for bust
            rewards[mask_bust] = -1                             # player loss
            return newstates, probs, rewards
        
        elif action == 1:                                       # player stick
            newstate = state.copy()
            newstate[0] = 1                                     # signal dealer turns
            return np.array([newstate]), 1, 0
        
        elif action == 2:                                       # dealer hit
            newstates[:, 3] += cards
            newstates[1, 4] += 1                                # add 1 usable ace            
            mask_bust = (newstates[:, 3] > 21)
            mask_usableace = (newstates[:, 4] > 0)            
            newstates[mask_bust & mask_usableace, 4] -= 1       # use up 1 ace
            newstates[mask_bust & mask_usableace, 3] -= 10      # sum reduce by 10
            mask_bust = (newstates[:, 3] > 21)
            newstates[mask_bust, 0] = 2                         # game end for bust
            rewards[mask_bust] = 1                              # player win
            return newstates, probs, rewards
        
        # dealer stick
        newstate = state.copy()
        newstate[0] = 2                                         # signal game end
        reward = np.sign(newstate[1] - newstate[3]) 
        return np.array([newstate]), 1, reward                  # 1 win, -1 loss, 0 draw
