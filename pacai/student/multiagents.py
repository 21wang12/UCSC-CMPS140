import random

from pacai.agents.base import BaseAgent
from pacai.agents.search.multiagent import MultiAgentSearchAgent

from pacai.core.distance import manhattan, maze

class ReflexAgent(BaseAgent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.
    You are welcome to change it in any way you see fit,
    so long as you don't touch the method headers.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        `ReflexAgent.getAction` chooses among the best options according to the evaluation function.

        Just like in the previous project, this method takes a
        `pacai.core.gamestate.AbstractGameState` and returns some value from
        `pacai.core.directions.Directions`.
        """

        # Collect legal moves.
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions.
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best.

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current `pacai.bin.pacman.PacmanGameState`
        and an action, and returns a number, where higher numbers are better.
        Make sure to understand the range of different values before you combine them
        in your evaluation function.
        """
        
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        # Useful information you can extract.
        # newPosition = successorGameState.getPacmanPosition()
        newFoods = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        # newScaredTimes = [ghostState.getScaredTimer() for ghostState in newGhostStates]

        # *** Your Code Here ***
        pacmanPosition = successorGameState.getPacmanPosition()
        dist2ClosestFood = 1e9
        newFoods = newFoods.asList()
        if pacmanPosition in newFoods: 
            newFoods = list(filter(lambda x: x != pacmanPosition, newFoods))
        for food in newFoods:
            # dist2ClosestFood = min(dist2ClosestFood, manhattan(food, pacmanPosition))
            dist2ClosestFood = min(dist2ClosestFood, maze(food, pacmanPosition, successorGameState))
        dist2ClosestGhost = 1e9
        SAFE_DISTANCE = 2
        for ghost in newGhostStates:
            if ghost.isBraveGhost() or ghost._scaredTimer * 2 < SAFE_DISTANCE:
                dist2ClosestGhost = min(dist2ClosestGhost, manhattan(ghost.getPosition(), pacmanPosition))
        if dist2ClosestGhost < SAFE_DISTANCE:
            dist2ClosestGhost = -1e9
        else:
            dist2ClosestGhost = 1e9
        return successorGameState.getScore() + (1.0 / dist2ClosestFood) + dist2ClosestGhost

class MinimaxAgent(MultiAgentSearchAgent):
    """
    A minimax agent.

    Here are some method calls that might be useful when implementing minimax.

    `pacai.core.gamestate.AbstractGameState.getNumAgents()`:
    Get the total number of agents in the game

    `pacai.core.gamestate.AbstractGameState.getLegalActions`:
    Returns a list of legal actions for an agent.
    Pacman is always at index 0, and ghosts are >= 1.

    `pacai.core.gamestate.AbstractGameState.generateSuccessor`:
    Get the successor game state after an agent takes an action.

    `pacai.core.directions.Directions.STOP`:
    The stop direction, which is always legal, but you may not want to include in your search.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, state):
        """
        Receive an `pacai.core.gamestate.AbstractGameState`.
        Return an action from `pacai.core.directions.Directions`.
        """
        ghosts = [i for i in range(1, state.getNumAgents())]  # pacman index is 0, other is ghost
        legalMoves = state.getLegalActions()
        bestScore = -1e9
        bestAction = None
        for action in legalMoves:
            successorState = state.generatePacmanSuccessor(action)
            score = self.minimax(successorState, 0, self.getEvaluationFunction(), True)
            if score > bestScore:
                bestScore = score
                bestAction = action
        return bestAction
    
    def minimax(self, state, depth, payoffFunction, isMaximizing):
        if state.isWin() or state.isLose() or depth == self.getTreeDepth():
            return payoffFunction(state)
        
        if isMaximizing:
            pass
        else:
            pass
        return payoffFunction(state) 


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    A minimax agent with alpha-beta pruning.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    An expectimax agent.

    All ghosts should be modeled as choosing uniformly at random from their legal moves.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the expectimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable evaluation function.

    DESCRIPTION: <write something here so we know what you did>
    """

    return currentGameState.getScore()

class ContestAgent(MultiAgentSearchAgent):
    """
    Your agent for the mini-contest.

    You can use any method you want and search to any depth you want.
    Just remember that the mini-contest is timed, so you have to trade off speed and computation.

    Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
    just make a beeline straight towards Pacman (or away if they're scared!)

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
