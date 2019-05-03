import numpy as np
from knapsack import KnapsackGame
from dna import DnaAlignGame
from dpsolver import DeterministicSolver

# Knapsack
items = np.array([2, 3, 1])
weights = np.array([5, 4, 2.5])
values = np.array([12, 11.5, 7])

game = KnapsackGame()
solver = DeterministicSolver(game)

state = game.reset(10, items, weights, values)
solver.solve(state)

print(solver.counter)
print(solver.cachedCounter)

# DNA Sequence Alignment
game = DnaAlignGame()
solver = DeterministicSolver(game)

x = 'TTCATA'
y = 'TGCTCGTA'
state = game.reset(x, y)
solver.solve(state)

# Blackjack
