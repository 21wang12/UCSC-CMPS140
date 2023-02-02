# Project 1: Search in Pac-Man

# Question 1

Implement the depth-first search (DFS) algorithm in `pacai.student.search.depthFirstSearch`. To make your algorithm complete, write the graph search version of DFS, which avoids expanding any already visited states (textbook section 3.5).

```python
def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first [p 85].
    """
    start = (problem.startingState(), None, 0)  # ((x, y), action, cost)
    frontier = Stack()
    frontier.push(start)
    visited = set()
    memory = dict()
    while not frontier.isEmpty():
        node = frontier.pop()
        if node[0] not in visited:
            visited.add(node[0])
            for neighbor in problem.successorStates(node[0]):
                if neighbor[0] not in visited:
                    memory[neighbor] = node
                    frontier.push(neighbor)
                if problem.isGoal(neighbor[0]):
                    path = []
                    # constrcut the path by memory
                    parent = neighbor
                    while parent[0] != start[0]:
                        path.append(parent[1])
                        parent = memory[parent]
                    return list(reversed(path))
    return []
```

# Question 2
Implement the breadth-first search (BFS) algorithm in `pacai.student.search.breadthFirstSearch`. Again, write a graph search algorithm that avoids expanding any already visited states. Test your code the same way you did for depth-first search.

```python
def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """
    start = (problem.startingState(), None, 0)  # ((x, y), action, cost)
    frontier = Queue()
    frontier.push(start)
    visited = set()
    memory = dict()
    while not frontier.isEmpty():
        node = frontier.pop()
        if node[0] not in visited:
            visited.add(node[0])
            for neighbor in problem.successorStates(node[0]):
                if neighbor[0] not in visited:
                    memory[neighbor] = node
                    frontier.push(neighbor)
                if problem.isGoal(neighbor[0]):
                    path = []
                    # constrcut the path
                    parent = neighbor
                    while parent[0] != start[0]:
                        path.append(parent[1])
                        parent = memory[parent]
                    return list(reversed(path))
    return []
```

# Question 3
Implement the uniform-cost graph search algorithm in `pacai.student.search.uniformCostSearch`. You should now observe successful behavior in all three of the following layouts. Here the agents are all UCS agents that differ only in the cost function they use (the agents and cost functions are written for you):

```python
def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """
    start = (problem.startingState(), None, 0)  # ((x, y), action, cost)
    frontier = PriorityQueue()
    frontier.push(start, start[2])
    visited = set()
    memory = dict()
    cost = dict()
    cost[start] = start[2]
    while not frontier.isEmpty():
        node = frontier.pop()
        if node[0] not in visited:
            visited.add(node[0])
            for neighbor in problem.successorStates(node[0]):
                if neighbor[0] not in visited:
                    memory[neighbor] = node
                    cost[neighbor] = neighbor[2] + cost[node]
                    frontier.push(neighbor, cost[neighbor])
                if problem.isGoal(neighbor[0]):
                    path = []
                    # constrcut the path
                    parent = neighbor
                    while parent[0] != start[0]:
                        path.append(parent[1])
                        parent = memory[parent]
                    return list(reversed(path))
    return []
```

# Question 4
Implement A* graph search algorithm in `pacai.student.search.aStarSearch`. A* takes a heuristic function as an argument. The heuristics function take two arguments: a state in the search problem (the main argument), and the problem itself (for reference information). The null heuristic is a trivial example.

You can test your A* implementation on the original problem of finding a path through a maze to a fixed position using the Manhattan distance heuristic. This heursitic is implemented for you already as `pacai.core.search.heuristic.manhattan`.

```python
def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    start = (problem.startingState(), None, 0)  # ((x, y), action, cost)
    frontier = PriorityQueue()
    frontier.push(start, start[2] + heuristic(start[0], problem))
    visited = set()
    memory = dict()
    cost = dict()
    cost[start] = start[2]
    while not frontier.isEmpty():
        node = frontier.pop()
        if node[0] not in visited:
            visited.add(node[0])
            for neighbor in problem.successorStates(node[0]):
                if neighbor[0] not in visited:
                    memory[neighbor] = node
                    cost[neighbor] = neighbor[2] + cost[node]
                    frontier.push(neighbor, cost[neighbor] + heuristic(neighbor[0], problem))
                if problem.isGoal(neighbor[0]):
                    path = []
                    # constrcut the path
                    parent = neighbor
                    while parent[0] != start[0]:
                        path.append(parent[1])
                        parent = memory[parent]
                    return list(reversed(path))
    return []
```

# Question 5
Implement the search problem `pacai.student.searchAgents.CornersProblem`. You will need to choose a state representation that encodes all the information necessary to detect whether all four corners have been reached.

To receive full credit, you need to define an abstract state representation that does not encode irrelevant information (like the position of ghosts, where extra food is, etc.). In particular, do not use a Pac-Man `PacmanGameState` as a search state. Your code will be very, very slow if you do (and also wrong).

Hint: The only parts of the game state you need to reference in your implementation are the starting Pac-Man position and the location of the four corners.

```python
class CornersProblem(SearchProblem):
    """
    This search problem finds paths through all four corners of a layout.
    """
    def __init__(self, startingGameState):
        super().__init__()

        self.walls = startingGameState.getWalls()
        self.startingPosition = startingGameState.getPacmanPosition()
        top = self.walls.getHeight() - 2
        right = self.walls.getWidth() - 2

        self.corners = ((1, 1), (1, top), (right, 1), (right, top))
        for corner in self.corners:
            if not startingGameState.hasFood(*corner):
                logging.warning('Warning: no food in corner ' + str(corner))
        self._numExpanded = 0

    def actionsCost(self, actions):
        """
        Returns the cost of a particular sequence of actions.
        If those actions include an illegal move, return 999999.
        This is implemented for you.
        """
        if (actions is None):
            return 999999

        x, y = self.startingPosition
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999

        return len(actions)

    def isGoal(self, state):
        """
        Returns whether this search state is a goal state of the problem.
        """
        position, unVisitedCorners = state
        return len(unVisitedCorners) == 0

    def startingState(self):
        """
        Returns the start state (in your search space,
        NOT a `pacai.core.gamestate.AbstractGameState`).
        """
        # Whether string position is on the one of the corner
        unVisitedCorners = tuple([corner for corner in self.corners
                                  if corner != self.startingPosition])
        return (self.startingPosition, unVisitedCorners)  # ((x,y), unVisiterdCorners)

    def successorStates(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.
        """
        successors = []
        self._numExpanded = self._numExpanded + 1
        for action in Directions.CARDINAL:
            position, unVisitedCorners = state
            x, y = position
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            hitsWall = self.walls[nextx][nexty]
            if (not hitsWall):
                nextPosition = (nextx, nexty)
                nextUnVisitedCorners = tuple([corner for corner in unVisitedCorners
                                              if corner != nextPosition])
                successors.append(((nextPosition, nextUnVisitedCorners), action, 1))
        return successors
```

# Question 6
Implement a heuristic for `CornersProblem` in `pacai.student.searchAgents.cornersHeuristic`.

Grading: inadmissible heuristics will get no credit.

+ 1 point for any admissible heuristic 
+ 2 point for expanding fewer than 1600 nodes 
+ 3 point for expanding fewer than 1200 nodes - [x]
+ Expand fewer than 800, and you're doing great!

```python
def cornersHeuristic(state, problem):
    """
    A heuristic for the CornersProblem that you defined.

    This function should always return a number that is a lower bound
    on the shortest path from the state to a goal of the problem;
    i.e. it should be admissible.
    (You need not worry about consistency for this heuristic to receive full credit.)
    """
    position, unVisitedCorners = state
    heuristicValue = 0
    for unVisitedCorner in unVisitedCorners:
        heuristicValue = max(heuristicValue, manhattan(position, unVisitedCorner))
    return heuristicValue  # Default to trivial solution
```

# Question 7
Implement a heuristic for `FoodSearchProblem` in `pacai.student.searchAgents.foodHeuristic`. 

Grading: inadmissible heuristics will get no credit

+ 1 point for expanding fewer than 15000 nodes (very easy) 
+ 2 point for expanding fewer than 12000 nodes (easy) 
+ 3 point for expanding fewer than 9000 nodes (medium) 
+ 4 point for expanding fewer than 7000 nodes (hard) - [x]

```python
def foodHeuristic(state, problem):
    """
    Your heuristic for the FoodSearchProblem goes here.
    """
    position, foodGrid = state
    value = 0
    foods = foodGrid.asList()
    for food in foods:
        # value = max(value, manhattan(position, food))
        value = max(value, maze(food, position, problem.startingGameState))
    return value
```

# Question 8
Implement the function `pacai.student.searchAgents.ClosestDotSearchAgent.findPathToClosestDot`.

```python
class ClosestDotSearchAgent(SearchAgent):
    """
    Search for all food using a sequence of searches.
    """
    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def registerInitialState(self, state):
        self._actions = []
        self._actionIndex = 0

        currentState = state

        while (currentState.getFood().count() > 0):
            nextPathSegment = self.findPathToClosestDot(currentState)  # The missing piece
            self._actions += nextPathSegment

            for action in nextPathSegment:
                legal = currentState.getLegalActions()
                if action not in legal:
                    raise Exception('findPathToClosestDot returned an illegal move: %s!\n%s' %
                            (str(action), str(currentState)))

                currentState = currentState.generateSuccessor(0, action)

        logging.info('Path found with cost %d.' % len(self._actions))

    def findPathToClosestDot(self, gameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from gameState.
        """
        problem = AnyFoodSearchProblem(gameState)
        return search.bfs(problem)

class AnyFoodSearchProblem(PositionSearchProblem):
    """
    A search problem for finding a path to any food.
    """
    def __init__(self, gameState, start = None):
        super().__init__(gameState, goal = None, start = start)

        # Store the food for later reference.
        self.food = gameState.getFood()

    def isGoal(self, state):
        return self.food[state[0]][state[1]]
```