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
            dist2ClosestFood = min(dist2ClosestFood, manhattan(food, pacmanPosition))
        dist2ClosestGhost = 1e9
        SAFE_DISTANCE = 2
        for ghost in newGhostStates:
            if ghost.isBraveGhost() or ghost._scaredTimer * 2 < SAFE_DISTANCE:
                dist2ClosestGhost = min(dist2ClosestGhost,
                                        manhattan(ghost.getPosition(), pacmanPosition))
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
        legalMoves = state.getLegalActions(0)  # PACMAN_AGENT_INDEX = 0
        bestScore = -1e9
        bestAction = None

        for action in legalMoves:
            successorState = state.generatePacmanSuccessor(action)
            score = self.minimax(successorState, 1,
                                 self.getEvaluationFunction(), 1, state.getNumGhosts())
            if score > bestScore:
                bestScore = score
                bestAction = action
        return bestAction

    def minimax(self, state, depth, payoffFunction, agentIndex, numGhosts=2):
        PACMAN_AGENT_INDEX = 0
        if state.isWin() or state.isLose() or depth == self.getTreeDepth():
            return payoffFunction(state)

        if agentIndex == PACMAN_AGENT_INDEX:
            legalMoves = state.getLegalActions(agentIndex)
            bestScore = -1e9
            for action in legalMoves:
                successorState = state.generateSuccessor(agentIndex, action)
                score = self.minimax(successorState, depth, payoffFunction,
                                     agentIndex + 1, numGhosts)
                if score > bestScore:
                    bestScore = score
            return bestScore
        elif agentIndex != numGhosts:
            legalMoves = state.getLegalActions(agentIndex)
            bestScore = 1e9
            for action in legalMoves:
                successorState = state.generateSuccessor(agentIndex, action)
                score = self.minimax(successorState, depth, payoffFunction,
                                     agentIndex + 1, numGhosts)
                if score < bestScore:
                    bestScore = score
            return bestScore
        else:
            legalMoves = state.getLegalActions(agentIndex)
            bestScore = 1e9
            for action in legalMoves:
                successorState = state.generateSuccessor(agentIndex, action)
                score = self.minimax(successorState, depth + 1,
                                     payoffFunction, 0, numGhosts)
                if score < bestScore:
                    bestScore = score
            return bestScore
        return None


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

    def getAction(self, state):
        bestScore = -1e9
        bestAction = None
        legalMoves = state.getLegalActions(0)
        for action in legalMoves:
            successorState = state.generatePacmanSuccessor(action)
            score = self.alphabeta(successorState, 1, self.getEvaluationFunction(),
                                   -1e9, 1e9, 1, state.getNumGhosts())
            if score > bestScore:
                bestScore, bestAction = score, action
        return bestAction

    def alphabeta(self, state, depth, payoffFunction, alpha, beta, agentIndex, numGhosts=2):
        if state.isWin() or state.isLose() or depth == self.getTreeDepth():
            return payoffFunction(state)
        if agentIndex == 0:
            legalMoves = state.getLegalActions(agentIndex)
            bestScore = -1e9
            for action in legalMoves:
                successorState = state.generateSuccessor(agentIndex, action)
                score = self.alphabeta(successorState, depth, payoffFunction,
                                       alpha, beta, agentIndex + 1, numGhosts)
                bestScore = max(bestScore, score)
                alpha = max(bestScore, alpha)
                if alpha >= beta:
                    break
            return bestScore
        elif agentIndex != numGhosts:
            legalMoves = state.getLegalActions(agentIndex)
            bestScore = 1e9
            for action in legalMoves:
                successorState = state.generateSuccessor(agentIndex, action)
                score = self.alphabeta(successorState, depth, payoffFunction,
                                       alpha, beta, agentIndex + 1, numGhosts)
                bestScore = min(bestScore, score)
                beta = min(bestScore, beta)
                if alpha >= beta:
                    break
            return bestScore
        else:
            legalMoves = state.getLegalActions(agentIndex)
            bestScore = 1e9
            for action in legalMoves:
                successorState = state.generateSuccessor(agentIndex, action)
                score = self.alphabeta(successorState, depth + 1, payoffFunction,
                                       alpha, beta, 0, numGhosts)
                bestScore = min(bestScore, score)
                beta = min(bestScore, beta)
                if alpha >= beta:
                    break
            return bestScore
        return None

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

    def getAction(self, state):
        bestScore = -1e9
        bestAction = None
        legalMoves = state.getLegalActions(0)
        for action in legalMoves:
            successorState = state.generatePacmanSuccessor(action)
            score = self.expectimax(successorState, 1, self.getEvaluationFunction(),
                                    1, state.getNumGhosts())
            if score > bestScore:
                bestScore, bestAction = score, action
        return bestAction

    def expectimax(self, state, depth, payoffFunction, agentIndex, numGhosts=2):
        PACMAN_AGENT_INDEX = 0
        if state.isWin() or state.isLose() or depth == self.getTreeDepth():
            return payoffFunction(state)
        if agentIndex == PACMAN_AGENT_INDEX:
            legalMoves = state.getLegalActions(agentIndex)
            bestScore = -1e9
            for action in legalMoves:
                successorState = state.generateSuccessor(agentIndex, action)
                score = self.expectimax(successorState, depth, payoffFunction,
                                        agentIndex + 1, numGhosts)
                if score > bestScore:
                    bestScore = score
            return bestScore
        elif agentIndex != numGhosts:
            legalMoves = state.getLegalActions(agentIndex)
            totalScore = 0
            for action in legalMoves:
                successorState = state.generateSuccessor(agentIndex, action)
                totalScore += self.expectimax(successorState, depth, payoffFunction,
                                              agentIndex + 1, numGhosts)
            return totalScore / len(legalMoves)
        else:
            legalMoves = state.getLegalActions(agentIndex)
            totalScore = 0
            for action in legalMoves:
                successorState = state.generateSuccessor(agentIndex, action)
                totalScore += self.expectimax(successorState, depth + 1,
                                              payoffFunction, 0, numGhosts)
            return totalScore / len(legalMoves)
        return None

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable evaluation function.

    DESCRIPTION: <write something here so we know what you did>
    """
    currentFoods = currentGameState.getFood().asList()
    currentGhostStates = currentGameState.getGhostStates()
    currentPacmanPosition = currentGameState.getPacmanPosition()
    dist2ClosestFood = 1e9
    for food in currentFoods:
        dist2ClosestFood = min(dist2ClosestFood,
                               maze(food, currentPacmanPosition, currentGameState))
    SAFE_DISTANCE = 3
    dist2ClosestGhost = 1e9
    for ghost in currentGhostStates:
        if ghost.isBraveGhost() or ghost._scaredTimer * 2 < SAFE_DISTANCE:
            dist2ClosestGhost = min(dist2ClosestGhost,
                                    manhattan(currentPacmanPosition, ghost.getPosition()))
    if dist2ClosestGhost < SAFE_DISTANCE:
        dist2ClosestGhost = -1000
    else:
        dist2ClosestGhost = 1000
    return currentGameState.getScore() + (1.0 / dist2ClosestFood) + dist2ClosestGhost

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
