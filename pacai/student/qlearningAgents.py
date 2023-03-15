from pacai.agents.learning.reinforcement import ReinforcementAgent
from pacai.util import reflection
from pacai.util import probability
from collections import defaultdict
import random

class QLearningAgent(ReinforcementAgent):
    """
    A Q-Learning agent.

    Some functions that may be useful:

    `pacai.agents.learning.reinforcement.ReinforcementAgent.getAlpha`:
    Get the learning rate.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.getDiscountRate`:
    Get the discount rate.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.getEpsilon`:
    Get the exploration probability.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.getLegalActions`:
    Get the legal actions for a reinforcement agent.

    `pacai.util.probability.flipCoin`:
    Flip a coin (get a binary value) with some probability.

    `random.choice`:
    Pick randomly from a list.

    Additional methods to implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Compute the action to take in the current state.
    With probability `pacai.agents.learning.reinforcement.ReinforcementAgent.getEpsilon`,
    we should take a random action and take the best policy action otherwise.
    Note that if there are no legal actions, which is the case at the terminal state,
    you should choose None as the action.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.update`:
    The parent class calls this to observe a state transition and reward.
    You should do your Q-Value update here.
    Note that you should never call this function, it will be called on your behalf.

    In Q learning, the pacman should explore the environment and learn the best policy.
    For each situation, the pacman should choose the best action to take.
    After each action, the pacman should update the Q value of the current state and action.
    To avoid the pacman getting stuck in a local minimum, the pacman should explore the environment
    by taking random actions.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

        # You can initialize Q-values here.
        self.q_values = dict()

    def getQValue(self, state, action):
        """
        Get the Q-Value for a `pacai.core.gamestate.AbstractGameState`
        and `pacai.core.directions.Directions`.
        Should return 0.0 if the (state, action) pair has never been seen.
        """
        if not (state, action) in self.q_values:
            return 0.0
        return self.q_values[(state, action)]

    def getValue(self, state):
        """
        Return the value of the best action in a state.
        I.E., the value of the action that solves: `max_action Q(state, action)`.
        Where the max is over legal actions.
        Note that if there are no legal actions, which is the case at the terminal state,
        you should return a value of 0.0.

        This method pairs with `QLearningAgent.getPolicy`,
        which returns the actual best action.
        Whereas this method returns the value of the best action.
        """
        legalMoves = self.getLegalActions(state)
        if len(legalMoves) == 0:
            return 0.0
        bestScore = -1e9
        for action in legalMoves:
            bestScore = max(bestScore, self.getQValue(state, action))
        return bestScore

    def getPolicy(self, state):
        """
        Return the best action in a state.
        I.E., the action that solves: `max_action Q(state, action)`.
        Where the max is over legal actions.
        Note that if there are no legal actions, which is the case at the terminal state,
        you should return a value of None.

        This method pairs with `QLearningAgent.getValue`,
        which returns the value of the best action.
        Whereas this method returns the best action itself.
        """
        legalMoves = self.getLegalActions(state)
        bestAction = None
        bestScore = -1e9
        for action in legalMoves:
            qvalue = self.getQValue(state, action)
            if qvalue > bestScore:
                bestScore = qvalue
                bestAction = action
        return bestAction

    def getAction(self, state):
        leagalMoves = self.getLegalActions(state)
        explore = probability.flipCoin(self.getEpsilon())
        if explore:
            return random.choice(leagalMoves)
        else:
            return self.getPolicy(state)

    def update(self, state, action, nextState, reward):
        old_Q = self.getQValue(state, action)
        alpha = self.getAlpha()
        gamma = self.getDiscountRate()
        self.q_values[(state, action)] = (1 - alpha) * old_Q +\
            alpha * (reward + gamma * self.getValue(nextState))

class PacmanQAgent(QLearningAgent):
    """
    Exactly the same as `QLearningAgent`, but with different default parameters.
    """

    def __init__(self, index, epsilon = 0.05, gamma = 0.8, alpha = 0.2, numTraining = 0, **kwargs):
        kwargs['epsilon'] = epsilon
        kwargs['gamma'] = gamma
        kwargs['alpha'] = alpha
        kwargs['numTraining'] = numTraining

        super().__init__(index, **kwargs)

    def getAction(self, state):
        """
        Simply calls the super getAction method and then informs the parent of an action for Pacman.
        Do not change or remove this method.
        """

        action = super().getAction(state)
        self.doAction(state, action)

        return action

class ApproximateQAgent(PacmanQAgent):
    """
    An approximate Q-learning agent.

    You should only have to overwrite `QLearningAgent.getQValue`
    and `pacai.agents.learning.reinforcement.ReinforcementAgent.update`.
    All other `QLearningAgent` functions should work as is.

    Additional methods to implement:

    `QLearningAgent.getQValue`:
    Should return `Q(state, action) = w * featureVector`,
    where `*` is the dotProduct operator.

    `pacai.agents.learning.reinforcement.ReinforcementAgent.update`:
    Should update your weights based on transition.

    Compare with `update` in `QLearningAgent`.
    `ApproximateQAgent` use features to represent the value of the Qstate.
    After each action, the pacman update the weight of each feature.
    """

    def __init__(self, index,
            extractor = 'pacai.core.featureExtractors.IdentityExtractor', **kwargs):
        super().__init__(index, **kwargs)
        self.featExtractor = reflection.qualifiedImport(extractor)

        # You might want to initialize weights here.
        self.weights = defaultdict(int)
        self.discount = self.getDiscountRate()

    def getQValue(self, state, action):
        total = 0
        features = self.featExtractor.getFeatures(self, state, action)
        for key in features:
            total += features[key] * self.weights[key]
        return total

    def update(self, state, action, nextState, reward):
        diff = (reward + self.discount * self.getValue(nextState)) - self.getQValue(state, action)
        features = self.featExtractor.getFeatures(self, state, action)
        for key in features:
            self.weights[key] = self.weights[key] + self.alpha * diff * features[key]

    def final(self, state):
        """
        Called at the end of each game.
        """

        # Call the super-class final method.
        super().final(state)
