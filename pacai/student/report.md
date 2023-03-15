# Problem definition
The very beging of our thought shows blow:

One pacman act as offensive pacman, Another one act as defensive pacman. The offensive pacman always want to eat all the dots of enemy and the defensive pacman always want to protect our dots.

At the beginning, we could fully utilize the 15 seconds in the initial start-up `registerInitialState` to calculate the `mazeDistance` for all the non-wall grid.

To quantify each move, we adopt `feature-based` metric to calculate the feature value of each move. We also define that the pacman always chose the move that can maximize the feature.

Next, the offensive pacman should go to the enemy area. To eat dot as quick as possible, the sum of distance feature for N dot should be calculated. The large the distance, the less the distance feature value. Due to the winning conditions, the N should more than 2. It is because the game ends when one team eats all but 2 of the opponents' dots. (Consider a state of 2 dots at the upper conner and 3 dots at the lower conner, we want the pacman to reach the lower conner and eat the 3 dot to win the game.)

The defensive pacman act almost the same as the offensive pacman, but the defensive pacman want to eat the enemy to protect our dots.

# Problem modeling

# Problem representation

# Computational strategy

# Algorithmic choice

# Obstacles

# Evaluation

# Lessons learned

