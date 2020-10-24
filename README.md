Generic Dynamic Programming Solver
===
Dynamic Programming (DP) is a techniques in both Applied Mathematics and Computer Science. It tries to find the optimal solution of a problem by breaking down the problem into smaller subproblems. There are many famous example problems to be solved by DP. This project picked the Knapsack problem, the DNA sequences alignment problem, as well as the game of Blackjack.

Traditionally, each DP problem is solved by a program specialized for the problem only. This project borrowed the idea of OpenAI Gym, a software developed for Reinforcement Learning (RL) simulation, to build a generic solver for all DP prolbems, which can be devided into deterministc DP problems and stochastic DP problems. The job of you is to code up the game object of yours, which communicates with the generic DP solver. The codes have shown you the examples of doing this. 

What are the similarities shared between Dynamic Programming (DP) and Reinforcement Learning (RL)? First of all, RL is the state-of-art technique for many famous AI applications that you may heard of, such as AlphaGo and Self-driving. DP and RL indeed both attempts to find the optimal sequence of actions of a problem. Previously, I have shown how to find the optimal policy in playing Blackjack with RL. In this project, I show you how to solve the same problem with DP. As you can see, being a relatively small problem like this, DP solves more faster, and the solution is guaranteed to be optimal, because DP attempts all possible solutions. However, if the state space of a problem is higher (Blackjack's dimension is two), DP would suffer from the Curse of Dimensionality. This comes to the opportunties for RL, because rather exploring all possible solutions, RL samples the poosible path of actions.

List of files
===

|File|Description|
|---|---|
|`dpsolver.py`|The core generic solver for determinstic DP and stochastic DP problems.
|`knapsack.py`|The demo shows you how to write the game object for the Knapsack problem, and call the solver.
|`dna.py`|The demo shows you how to write the game object for the DNA sequences alignment, and call the solver.
|`blackjack.py`|The demo shows you how to write the game oject for the Blackjack game, which is a stochastic DP problem.
|`blackjack_results.py`|Visualize the optimal policy for the Blackjack game.

Instructions
===
1. Install the following packages:
  - python (3.6.8)
  - numpy (1.16.4)
  - pandas (0.24.2)
  - matplotlib (3.1.0)
  - seaborn (0.9.0)

### Deterministic DP Solver
2. Inspect the codes in `knapsack.py`, run `python knapsack.py` to see the solution.
3. Inspect the codes in `dna.py`, run `python dna.py` to see the solution.

### Stochastic DP Solver
4. Inspect the codes in `blackjack.py`
5. Open and run `blackjack_results.py` in an IDE, e.g. Spyder, to visualize the solution.
