from pacai.util import reflection

from collections import defaultdict
from pacai.core.directions import Directions
from pacai.bin.capture import CaptureGameState
from pacai.agents.capture.capture import CaptureAgent
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

    def getFeatures(self, gameState, action):
        features = {}
        successor = self.getSuccessor(gameState, action)
        features['successorScore'] = self.getScore(successor)

        # Compute distance to the nearest food.
        foodList = self.getFood(successor).asList()

        # This should always be True, but better safe than sorry.
        if (len(foodList) > 0):
            myPos = successor.getAgentState(self.index).getPosition()
            minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
            features['distanceToFood'] = minDistance
            
        oppoentsGhostStates = [gameState.getAgentStates()[i] for i in self.getOpponents(gameState) 
                              if gameState.isOnBlueSide(gameState.getAgentStates()[i].getPosition())]
        oppoentsPacmanStates = [gameState.getAgentStates()[i] for i in self.getOpponents(gameState) 
                              if gameState.isOnRedSide(gameState.getAgentStates()[i].getPosition())]
        
        teamGhostStates = [gameState.getAgentStates()[i] for i in self.getTeam(gameState) 
                              if gameState.isOnRedSide(gameState.getAgentStates()[i].getPosition())]
        teamPacmanStates = [gameState.getAgentStates()[i] for i in self.getTeam(gameState) 
                              if gameState.isOnBlueSide(gameState.getAgentStates()[i].getPosition())]
        if(len(oppoentsGhostStates) > 0):
            myPos = successor.getAgentState(self.index).getPosition()
            minDistance = min([self.getMazeDistance(myPos, oppoentsGhostState.getPosition()) for oppoentsGhostState in oppoentsGhostStates])
            features['distanceToGhost'] = minDistance
        
        return features

    def getWeights(self, gameState, action):
        return {
            'successorScore': 100,
            'distanceToFood': -1,
            'distanceToGhost': 0.1
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
            'reverse': -2
        }



class myCaptureAgent(CaptureAgent):
    def __init__(self, index, timeForComputing=0.1, **kwargs):
        super().__init__(index, timeForComputing, **kwargs)
        self.treeDepth = 3
        
    def registerInitialState(self, gameState):
        super().registerInitialState(gameState)
    
    def chooseAction(self, state):
        bestScore = -1e9
        bestAction = None
        legalMoves = state.getLegalActions(self.index)
        for action in legalMoves:
            successorState = state.generateSuccessor(self.index, action)
            score = self.expectimax(successorState, 1, self.betterEvaluationFunction,
                                    self.getTeam(state)[1])
            if score > bestScore:
                bestScore, bestAction = score, action
        return bestAction
    
    def expectimax(self, state, depth, payoffFunction, agentIndex):
        if state.isOver() or depth == self.treeDepth:
            return payoffFunction(state)
        if agentIndex == self.getTeam(state)[0]:
            legalMoves = state.getLegalActions(agentIndex)
            bestScore = -1e9
            for action in legalMoves:
                successorState = state.generateSuccessor(agentIndex, action)
                score = self.expectimax(successorState, depth, payoffFunction,
                                        self.getTeam(state)[1])
                if score > bestScore:
                    bestScore = score
            return bestScore
        elif agentIndex == agentIndex == self.getTeam(state)[1]:
            legalMoves = state.getLegalActions(agentIndex)
            bestScore = -1e9
            for action in legalMoves:
                successorState = state.generateSuccessor(agentIndex, action)
                score = self.expectimax(successorState, depth, payoffFunction,
                                        self.getOpponents(state)[0])
                if score > bestScore:
                    bestScore = score
            return bestScore
        elif agentIndex == self.getOpponents(state)[0]:
            legalMoves = state.getLegalActions(agentIndex)
            totalScore = 0
            for action in legalMoves:
                successorState = state.generateSuccessor(agentIndex, action)
                totalScore += self.expectimax(successorState, depth, payoffFunction,
                                              self.getOpponents(state)[1])
            return totalScore / len(legalMoves)
        elif agentIndex == self.getOpponents(state)[1]:
            legalMoves = state.getLegalActions(agentIndex)
            totalScore = 0
            for action in legalMoves:
                successorState = state.generateSuccessor(agentIndex, action)
                totalScore += self.expectimax(successorState, depth + 1, payoffFunction,
                                              self.getTeam(state)[0])
            return totalScore / len(legalMoves)
        return None
    
    def betterEvaluationFunction(self, currentGameState: CaptureGameState):
        currentFoods = self.getFood(currentGameState).asList()
        
        oppoentsGhostStates = [currentGameState.getAgentStates()[i] for i in self.getOpponents(currentGameState) 
                              if currentGameState.isOnBlueSide(currentGameState.getAgentStates()[i].getPosition())]
        oppoentsPacmanStates = [currentGameState.getAgentStates()[i] for i in self.getOpponents(currentGameState) 
                              if currentGameState.isOnRedSide(currentGameState.getAgentStates()[i].getPosition())]
        
        teamGhostStates = [currentGameState.getAgentStates()[i] for i in self.getTeam(currentGameState) 
                              if currentGameState.isOnRedSide(currentGameState.getAgentStates()[i].getPosition())]
        teamPacmanStates = [currentGameState.getAgentStates()[i] for i in self.getTeam(currentGameState) 
                              if currentGameState.isOnBlueSide(currentGameState.getAgentStates()[i].getPosition())]
        
        currAgentPosition = currentGameState.getAgentStates()[self.index].getPosition()
        dist2ClosestFood = 1e6
        for food in currentFoods:
            dist2ClosestFood = min(dist2ClosestFood,
                                self.distancer.getDistance(currAgentPosition, food))
        SAFE_DISTANCE = 3
        dist2ClosestGhost = 1e6
        dist2ClosestScaryGhost = 1e6
        for ghost in oppoentsGhostStates:
            if ghost.isBraveGhost() or ghost._scaredTimer * 2 < SAFE_DISTANCE:
                dist2ClosestGhost = min(dist2ClosestGhost,
                                        self.distancer.getDistance(currAgentPosition, ghost.getPosition()))
        if dist2ClosestGhost < SAFE_DISTANCE:
            dist2ClosestGhost = -1000
        else:
            dist2ClosestGhost = 0
        for ghost in oppoentsGhostStates:
            if not ghost.isBraveGhost() or not ghost._scaredTimer * 2 < SAFE_DISTANCE:
                dist2ClosestScaryGhost = min(dist2ClosestScaryGhost,
                                        self.distancer.getDistance(currAgentPosition, ghost.getPosition()))
        if dist2ClosestScaryGhost < SAFE_DISTANCE:
            dist2ClosestScaryGhost = 10 / (dist2ClosestScaryGhost+1)
        else:
            dist2ClosestScaryGhost = 0
        distInTeam = 0
        if len(teamPacmanStates) == 2:
            distInTeam = self.distancer.getDistance(teamPacmanStates[0].getPosition(), teamPacmanStates[1].getPosition())
        
        return currentGameState.getScore() + (1.0 / dist2ClosestFood) \
            + dist2ClosestGhost + 0.01 * distInTeam