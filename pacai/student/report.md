# Problem definition
The very beging of our thought shows blow:

One pacman act as offensive pacman, Another one act as defensive pacman. The offensive pacman always want to eat all the dots of enemy and the defensive pacman always want to protect our dots.

At the beginning, we utilize the 15 seconds in the initial start-up `registerInitialState` to calculate the `mazeDistance` for all the non-wall grid. We notice that the `distancer` in `CaptureAgent` has done this job. 

To quantify each move, we adopt `feature-based` metric to calculate the feature value of each move. We also define that the pacman always chose the move that can maximize the feature.

Next, the offensive pacman should go to the enemy area. To eat dot as quick as possible, the sum of distance feature for N dot should be calculated. The large the distance, the less the distance feature value. Due to the winning conditions, the N should more than 2. It is because the game ends when one team eats all but 2 of the opponents' dots. (Consider a state of 2 dots at the upper conner and 3 dots at the lower conner, we want the pacman to reach the lower conner and eat the 3 dot to win the game.)

The defensive pacman act almost the same as the offensive pacman, but the defensive pacman want to eat the enemy to protect our dots.

# Problem modeling
The offensive and defensive agents are based on `ReflexCaptureAgent`. The `ReflexCaptureAgent` used a feature-based policy to calculate each feature value for each legal move in current game state.

Initially, the offensive agent in baseline team considers the `successorScore` and `distanceToFood` to calculate the feature value for each move. We want our agent more flexible. Therefore, we take `distanceToOpponentGhost`, `distanceToOpponentPacman`, `distanceToCapsule`, `stop`, and `reverse` features into account. The meaning of each feature is described as below:
+ `distanceToOpponentGhost`: The agent should keep away from opponents ghost.
+ `distanceToOpponentPacman`: When the agent is currently in its own area and there is one or more than one invader, the agent should eat the invaders before go to opponent area if the invaders is close to itself.
+ `distanceToCapsule`: The capsule should have more priority to be eaten than the food.
+ `stop`: We do not want the agent should not stop all the time.
+ `reverse`: We also do not want the agent go back to the road it goes last time.


The defensive agent in baseline team considers the `onDefense`, `invaderDistance`, `stop`, `reverse`, and `numInvaders`. To make it more flexible, and catch the invaders as soon as possible, we take the `center` into account in defensive agent, which means that if there is no invader, the agent should go to the center of the game board. Using this feature, we can block the baseline offensive agent from eating our food.
# Problem representation


# Algorithmic choice

# Obstacles

# Evaluation




# Lessons learned

