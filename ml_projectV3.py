import collections
import math
import random
from queue import PriorityQueue

class Maze:
    def __init__(self, inputString):
        self.maze_matrix = []
        counter = 0
        for row in inputString.split('\n'):
            maze_row = []
            maze_row.extend(row)
            counter += 1
            self.maze_matrix.append(maze_row)

    def get(self, position):
        x, y = position
        val = self.maze_matrix[y][x]
        return val

    def printMaze(self, position):
        x, y = position
        for i in range(len(self.maze_matrix)):
            row = []
            for j in range(len(self.maze_matrix[i])):
                if (i == y and j == x):
                    row.append("+")
                else:
                    row.append(self.maze_matrix[i][j])
            print(row)

    def findGoal(self):
        for y in range(len(self.maze_matrix)):
            for x in range(len(self.maze_matrix[y])):
                if self.maze_matrix[y][x] == 'O':
                    return x, y

    def distCalc(self, position):
        goalX, goalY = self.findGoal()
        x, y = position
        dist = abs(goalX - x) + abs(goalY - y)
        return dist

    def is_obstacle(self, position):
        x, y = position
        return self.maze_matrix[y][x] == 'X'




class State:
    def __init__(self, maze, pos):
        self.maze = maze
        self.position = pos
        self.path = [pos]

    def __hash__(self):
        return hash(self.position)

    def printString(self):
        print("Current Maze State:")
        print("Position:", self.position)
        self.maze.printMaze(self.position)
        print("Path:", self.path)  # Print the path


class Problem:
    def __init__(self, initial):
        self.initialState = initial

    def actions(self, currentState):
        actions = ["up", "down", "left", "right"]
        x, y = currentState.position 
        if self.initialState.maze.get((x + 1, y)) == 'X':
            actions.remove("right")
        if self.initialState.maze.get((x - 1, y)) == 'X':
            actions.remove("left")
        if self.initialState.maze.get((x, y + 1)) == 'X':
            actions.remove("down")
        if self.initialState.maze.get((x, y - 1)) == 'X':
            actions.remove("up")
        return actions

    def takeAction(self, currentState, chosenAction):
        x, y = currentState.position
        if chosenAction == "right":
            returnPosition = (x + 1, y)
        if chosenAction == "left":
            returnPosition = (x - 1, y)
        if chosenAction == "up":
            returnPosition = (x, y - 1)
        if chosenAction == "down":
            returnPosition = (x, y + 1)
        return State(currentState.maze, returnPosition)

    def testForGoal(self, currentState):
        x, y = currentState.position  
        if self.initialState.maze.get((x, y)) == 'O':
            return True
        else:
            return False



class Node:
    def __init__(self, state, parentNode=None, action=None, parentCost=0):
        self.state = state
        self.parent = parentNode
        self.action = action
        self.estimatedCost = self.state.maze.distCalc(self.state.position)
        self.costToPresent = parentCost
        self.totalEstimation = self.estimatedCost + self.costToPresent
        self.depth = 0
        if parentNode:
            self.depth = parentNode.depth + 1

    def childNodes(self, problem, action):
        nextState = problem.takeAction(self.state, action)
        nextNode = Node(nextState, self, action, self.costToPresent + 1)
        return nextNode

    def expand(self, problem):
        returnNodes = []
        for action in problem.actions(self.state):
            returnNodes.append(self.childNodes(problem, action))
        return returnNodes


class RRTNode:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent

def BuildRRT(maze, qinit, K, Δq):
    G = []  # Initialize the RRT as a list of nodes
    G.append(RRTNode(qinit))

    for k in range(K):
        qrand = (random.randint(0, len(maze.maze_matrix[0]) - 1), random.randint(0, len(maze.maze_matrix) - 1))
        qnear = G[0]
        min_dist = maze.distCalc(qrand)  # Call distCalc with one argument

        for node in G:
            dist = maze.distCalc(node.position)  # Call distCalc with one argument
            if dist < min_dist:
                min_dist = dist
                qnear = node

        qnew = NEW_CONF(qnear.position, qrand, Δq, maze)
        if not maze.is_obstacle(qnew):  # Check if the new configuration is not in an obstacle
            G.append(RRTNode(qnew, parent=qnear))


    return G

def NEW_CONF(qnear, qrand, Δq, maze):
    # Interpolate between qnear and qrand by Δq steps
    delta_x = qrand[0] - qnear[0]
    delta_y = qrand[1] - qnear[1]
    distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
    if distance <= Δq:
        return qrand  # qrand is reachable within Δq

    # Calculate the unit vector from qnear to qrand
    unit_x = delta_x / distance
    unit_y = delta_y / distance

    # Calculate the new configuration qnew
    qnew_x = qnear[0] + Δq * unit_x
    qnew_y = qnear[1] + Δq * unit_y

    qnew = (int(qnew_x), int(qnew_y))
    return qnew

# Add the following method to the Maze class
def is_obstacle(self, position):
    j, i = position
    return self.maze_matrix[i][j] == 'X'


# Define a helper function to retrieve the path from the RRT graph
def extract_path(node):
    path = []
    while node:
        path.append(node.position)
        node = node.parent
    return path[::-1]

# Add a printPath function to print the path taken by the RRT
def printPath(rrt_graph):
    for i, node in enumerate(rrt_graph):
        path = extract_path(node)
        print(f"Step {i}: Path -> {path}")

def printGraphMazeStepByStep(maze, rrt_graph):
    for i, node in enumerate(rrt_graph):
        path = extract_path(node)
        print("Step", i, "Path:", path)
        for y in range(len(maze.maze_matrix)):
            row = []
            for x in range(len(maze.maze_matrix[y])):
                if (x, y) in path:
                    row.append("*")  # Represent path as *
                else:
                    row.append(maze.maze_matrix[y][x])
            print("".join(row))


maze1 = """XXXXXXXXXXXXXXX
X.............X
X.............X
X......O......X
X.............X
X.............X
X.............X
XXXXXXXXXXXXXXX"""

startingPosition = (1,1)
maze1_Init = Maze(maze1)
maze1_State = State(maze1_Init, startingPosition)
maze1_Problem = Problem(maze1_State)

K = 300 # Number of vertices in the RRT
Δq = 1  # Incremental distance

rrt_graph = BuildRRT(maze1_Init, startingPosition, K, Δq)
printGraphMazeStepByStep(maze1_Init, rrt_graph)  # Print the maze with RRT nodes step by step
