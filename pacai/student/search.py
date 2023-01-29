"""
In this file, you will implement generic search algorithms which are called by Pacman agents.

Important note: All of your search functions need to return a list of actions that will lead 
the agent from the start to the goal. These actions all have to be legal moves (valid directions, 
no moving through walls).
"""

from pacai.util.stack import Stack
from pacai.util.priorityQueue import PriorityQueue
from pacai.util.queue import Queue

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first [p 85].

    Your search algorithm needs to return a list of actions that reaches the goal.
    Make sure to implement a graph search algorithm [Fig. 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    ```
    print("Start: %s" % (str(problem.startingState())))
    print("Is the start a goal?: %s" % (problem.isGoal(problem.startingState())))
    print("Start's successors: %s" % (problem.successorStates(problem.startingState())))
    ```
    """
    start = (problem.startingState(), None, 0)
    if problem.isGoal(start[0]):
        return []
    frontier = Stack()
    frontier.push(start)
    visited = set()
    memory = dict()
    while not frontier.isEmpty():
        node = frontier.pop()
        visited.add(node[0])
        for neighbor in problem.successorStates(node[0]):
            if neighbor[0] not in visited:
                memory[neighbor] = node
                if problem.isGoal(neighbor[0]):
                    path = []
                    # constrcut the path
                    parent = neighbor
                    while parent[0] != start[0]:
                        path.append(parent[1])
                        parent = memory[parent]
                    return list(reversed(path))
                frontier.push(neighbor)
    return []

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """
    start = (problem.startingState(), None, 0)
    if problem.isGoal(start[0]):
        return []
    frontier = Queue()
    frontier.push(start)
    visited = set()
    memory = dict()
    while not frontier.isEmpty():
        node = frontier.pop()
        visited.add(node[0])
        for neighbor in problem.successorStates(node[0]):
            if neighbor[0] not in visited:
                memory[neighbor] = node
                if problem.isGoal(neighbor[0]):
                    path = []
                    # constrcut the path
                    parent = neighbor
                    while parent[0] != start[0]:
                        path.append(parent[1])
                        parent = memory[parent]
                    return list(reversed(path))
                frontier.push(neighbor)
    return []

def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """
    start = (problem.startingState(), None, 0)
    if problem.isGoal(start[0]):
        return []
    frontier = PriorityQueue()
    frontier.push(start, start[2])
    visited = set()
    memory = dict()
    cost = dict()
    cost[start] = start[2]
    while not frontier.isEmpty():
        node = frontier.pop()
        visited.add(node[0])
        for neighbor in problem.successorStates(node[0]):
            if neighbor[0] not in visited:
                memory[neighbor] = node
                cost[neighbor] = cost[node] + neighbor[2]
                if problem.isGoal(neighbor[0]):
                    path = []
                    # constrcut the path
                    parent = neighbor
                    while parent[0] != start[0]:
                        path.append(parent[1])
                        parent = memory[parent]
                    return list(reversed(path))
                frontier.push(neighbor, cost[neighbor])
    return []

# def aStarSearch(problem, heuristic):
#     """
#     Search the node that has the lowest combined cost and heuristic first.
#     """
#     start = (problem.startingState(), None, 0)
#     if problem.isGoal(start[0]):
#         return []
#     frontier = PriorityQueue()
#     frontier.push(start, start[2] + heuristic(start[0], problem))
#     visited = set()
#     memory = dict()
#     cost = dict()
#     cost[start] = start[2]
#     while not frontier.isEmpty():
#         node = frontier.pop()
#         visited.add(node[0])
#         for neighbor in problem.successorStates(node[0]):
#             if neighbor[0] not in visited:
#                 memory[neighbor] = node
#                 cost[neighbor] = cost[node] + neighbor[2]
#                 if problem.isGoal(neighbor[0]):
#                     path = []
#                     # constrcut the path
#                     parent = neighbor
#                     while parent[0] != start[0]:
#                         path.append(parent[1])
#                         parent = memory[parent]
#                     return list(reversed(path))
#                 frontier.push(neighbor, cost[neighbor] + heuristic(neighbor[0], problem))
#     return []

def aStarSearch(problem, heuristic):
    frontier = PriorityQueue()
    visited = set()

    frontier.push((problem.startingState(), [], 0), 0)

    while not frontier.isEmpty():
        node, path, priority = frontier.pop()
        
        if problem.isGoal(node):
            return path

        if node not in visited:
            visited.add(node)
            for successor in problem.successorStates(node):
                frontier.push((successor[0], path + [successor[1]], successor[2] + priority),\
                    successor[2] + priority + heuristic(successor[0], problem))

    return []