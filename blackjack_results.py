"""
blackjack_results.py
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D
import seaborn as sns
from blackjack import BlackjackGame
from dpsolver import StochasticSolver

game = BlackjackGame()
solver = StochasticSolver(game)

# Solve without usable ace cases
policy = np.zeros((20, 10))
values = np.zeros((20, 10))
for playersum in np.arange(4, 21):
    for dealercard in np.arange(1, 11):
        init = game.reset(0, playersum, dealercard)
        value, optimal = solver.solve(init)
        policy[playersum-1, dealercard-1] = optimal
        values[playersum-1, dealercard-1] = value

# Plot policy diagram
df = pd.DataFrame(policy[3:])
df.columns = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10]
df.index = np.arange(4, 21)

fig = plt.figure(figsize=(3,6))
ax = sns.heatmap(df, cmap='gray', cbar=False, linecolor='black', linewidths=0.1, vmin=-1, vmax=1)
ax.invert_yaxis()
ax.set_xlabel('Dealer Card')
ax.set_ylabel('Player Sum')
ax.set_title('Player Policy (/wo Usable Ace)')

# Plot state values 3D
fig = plt.figure(figsize=(10,8))
x = np.arange(3, 20)
y = np.arange(0, 10)
X, Y = np.meshgrid(x, y)

Z = values[X, Y]
ax = plt.axes(projection='3d')
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis')
ax.view_init(40, -90)
ax.set_xticks(np.arange(4, 21, 2))
ax.set_yticks(np.arange(1, 11, 2))
ax.set_xlabel('Player Sum')
ax.set_ylabel('Dealer Card')
ax.set_zlabel('State Value')
ax.invert_yaxis()
ax.set_title('/wo Usable Ace')
plt.show()

# Solve usable ace cases
policy = np.zeros((20, 10))
values = np.zeros((20, 10))
for playersum in np.arange(12, 21):
    for dealercard in np.arange(1, 11):
        init = game.reset(1, playersum, dealercard)
        value, optimal = solver.solve(init)
        policy[playersum-1, dealercard-1] = optimal
        values[playersum-1, dealercard-1] = value

# Plot policy diagram
df = pd.DataFrame(policy[11:])
df.columns = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10]
df.index = np.arange(12, 21)

fig = plt.figure(figsize=(3,3))
ax = sns.heatmap(df, cmap='gray', cbar=False, linecolor='black', linewidths=0.1, vmin=-1, vmax=1)
ax.invert_yaxis()
ax.set_xlabel('Dealer Card')
ax.set_ylabel('Player Sum')
ax.set_title('Player Policy (/w Usable Ace)')

# Plot state values 3D
fig = plt.figure(figsize=(10,8))
x = np.arange(3, 20)
y = np.arange(0, 10)
X, Y = np.meshgrid(x, y)

Z = values[X, Y]
ax = plt.axes(projection='3d')
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis')
ax.view_init(40, -90)
ax.set_xticks(np.arange(4, 21, 2))
ax.set_yticks(np.arange(1, 11, 2))
ax.set_xlabel('Player Sum')
ax.set_ylabel('Dealer Card')
ax.set_zlabel('State Value')
ax.invert_yaxis()
ax.set_title('/w Usable Ace')
plt.show()

# Nodes visited
print(solver.counter)
print(solver.cachedCounter)

