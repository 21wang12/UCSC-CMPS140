from pacai.util import reflection

from pacai.core.directions import Directions
from pacai.agents.capture.reflex import ReflexCaptureAgent

def createTeam(firstIndex, secondIndex, isRed,
        first = 'pacai.student.myTeam.myOffensiveReflexAgent',
        second = 'pacai.student.myTeam.myDefensiveReflexAgent'):
    """
    This function should return a list of two agents that will form the capture team,
    initialized using firstIndex and secondIndex as their agent indexed.
    isRed is True if the red team is being created,
    and will be False if the blue team is being created.
    """

    firstAgent = reflection.qualifiedImport(first)
    secondAgent = reflection.qualifiedImport(second)

    return [
        firstAgent(firstIndex),
        secondAgent(secondIndex),
    ]

class myOffensiveReflexAgent(ReflexCaptureAgent):
    def __init__(self, index, **kwargs):
        super().__init__(index)
        self.safeDistance = 2
        self.btwDistance = 3
        self.capsuleDistance = 1

    def getFeatures(self, currentGameState, action):
        features = {}
        successorGameState = self.getSuccessor(currentGameState, action)
        features['successorScore'] = self.getScore(successorGameState)
        foodList = self.getFood(successorGameState).asList()

        # agentCurrentPos = currentGameState.getAgentState(self.index).getPosition()
        # agentSuccessorPos = successorGameState.getAgentState(self.index).getPosition()

        mySuccessorPos = successorGameState.getAgentState(self.index).getPosition()
        # myCurrentPos = currentGameState.getAgentState(self.index).getPosition()

        # This should always be True, but better safe than sorry.
        if (len(foodList) > 0):
            foodList += self.getCapsules(currentGameState)
            minDistance = min([self.getMazeDistance(mySuccessorPos, food) for food in foodList])
            features['distanceToFood'] = minDistance

        currentOppoentsGhostStates = [currentGameState.getAgentStates()[i]
                                      for i in self.getOpponents(currentGameState)
                              if currentGameState.getAgentStates()[i].isGhost()]
        successorOppoentsPacmanStates = [successorGameState.getAgentStates()[i]
                                         for i in self.getOpponents(successorGameState)
                              if successorGameState.getAgentStates()[i].isPacman()]

        currentCapsules = self.getCapsules(currentGameState)

        if (action == Directions.STOP):
            features['stop'] = 1

        rev = Directions.REVERSE[currentGameState.getAgentState(self.index).getDirection()]
        if (action == rev):
            features['reverse'] = 1

        if(len(currentOppoentsGhostStates) > 0):
            if len([self.getMazeDistance(mySuccessorPos,
                                         oppoentsGhostState.getPosition())
                    for oppoentsGhostState in currentOppoentsGhostStates
                    if not oppoentsGhostState.isScared()]) > 0:
                minDistance = min([self.getMazeDistance(mySuccessorPos,
                                                        oppoentsGhostState.getPosition())
                                   for oppoentsGhostState in currentOppoentsGhostStates
                                   if not oppoentsGhostState.isScared()])
                if minDistance <= self.safeDistance and \
                        currentGameState.getAgentState(self.index).isPacman():
                    features['distanceToOpponentGhost'] = minDistance
                else:
                    features['distanceToOpponentGhost'] = self.safeDistance

        if(len(currentCapsules) > 0):
            minDistance = min([self.getMazeDistance(mySuccessorPos, currentCapsule)
                               for currentCapsule in currentCapsules])
            if minDistance <= self.capsuleDistance:
                features['distanceToCapsule'] = 1 / (minDistance + 1)

        if(len(successorOppoentsPacmanStates) > 0):
            minDistance = min([self.getMazeDistance(mySuccessorPos,
                                                    oppoentsPacmanState.getPosition())
                               for oppoentsPacmanState in successorOppoentsPacmanStates])
            if minDistance <= self.btwDistance:
                features['distanceToOpponentPacman'] = minDistance
            else:
                features['distanceToOpponentPacman'] = self.btwDistance
        return features

    def getWeights(self, gameState, action):
        return {
            'successorScore': 100,
            'distanceToFood': -1,
            'distanceToOpponentGhost': 2,
            'distanceToOpponentPacman': -2,
            'distanceToCapsule': 2,
            'stop': -100,
            'reverse': -2,
        }

class myDefensiveReflexAgent(ReflexCaptureAgent):
    """
    A reflex agent that tries to keep its side Pacman-free.
    This is to give you an idea of what a defensive agent could be like.
    It is not the best or only way to make such an agent.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index)

    def getFeatures(self, gameState, action):
        features = {}

        successor = self.getSuccessor(gameState, action)
        myState = successor.getAgentState(self.index)
        myPos = myState.getPosition()

        # Computes whether we're on defense (1) or offense (0).
        features['onDefense'] = 1
        if (myState.isPacman()):
            features['onDefense'] = 0

        # Computes distance to invaders we can see.
        enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        invaders = [a for a in enemies if a.isPacman() and a.getPosition() is not None]
        features['numInvaders'] = len(invaders)

        if (len(invaders) > 0):
            dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
            features['invaderDistance'] = min(dists)
        else:
            width = gameState.getWalls()._width
            height = gameState.getWalls()._height
            wallList = gameState.getWalls().asList()
            center = None
            for i in range(int(width / 2) - 3, int(width / 2)):
                for j in range(int(height / 2) - 3, int(height / 2) + 3):
                    if i <= 1 or i >= width / 2 or j <= 1 or j >= height:
                        continue
                    if not (i, j) in wallList:
                        center = (i, j)
            features['center'] = self.getMazeDistance(myPos, center)

        if (action == Directions.STOP):
            features['stop'] = 1

        rev = Directions.REVERSE[gameState.getAgentState(self.index).getDirection()]
        if (action == rev):
            features['reverse'] = 1

        return features

    def getWeights(self, gameState, action):
        return {
            'numInvaders': -1000,
            'onDefense': 100,
            'invaderDistance': -10,
            'stop': -100,
            'reverse': -2,
            'center': -3
        }
