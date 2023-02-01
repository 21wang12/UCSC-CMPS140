# Project 1: Search in Pac-Man

# Question 1

Implement the depth-first search (DFS) algorithm in `pacai.student.search.depthFirstSearch`. To make your algorithm complete, write the graph search version of DFS, which avoids expanding any already visited states (textbook section 3.5).

```python
def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.
    """
    start = (problem.startingState(), None, 0) # ((x, y), action, cost)
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
                if problem.isGoal(node[0]):
                    path = []
                    # constrcut the path
                    parent = node
                    while parent[0] != start[0]:
                        path.append(parent[1])
                        parent = memory[parent]
                    return list(reversed(path))
    return []
```