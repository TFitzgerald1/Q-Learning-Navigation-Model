import collections
import math
from queue import PriorityQueue

class Maze:
  def __init__(self,inputString):
    self.maze_matrix = []
    counter = 0
    for row in inputString.split('\n'):
      maze_row = []
      maze_row.extend(row)
      counter+=1
      self.maze_matrix.append(maze_row)
    
    for i in range(len(self.maze_matrix)): # Y-AXIS 0 at top
      row = []
      for j in range(len(self.maze_matrix[i])): # X-AXIS 0 at left
          row.append(self.maze_matrix[i][j])
      print(row)
          
  def get(self, position):
    j,i = position
    val = self.maze_matrix[i][j]
    return val
  def printMaze(self, position):
    x,y = position
    for i in range(len(self.maze_matrix)): # Y-AXIS 0 at top
      row = []
      for j in range(len(self.maze_matrix[i])): # X-AXIS 0 at left
        if (i == y and j == x):
          row.append("+")
        else:
          row.append(self.maze_matrix[i][j])
      print(row)
  def findGoal(self):
    for y in range(len(self.maze_matrix)): # Y-AXIS 0 at top
      for x in range(len(self.maze_matrix[y])): # X-AXIS 0 at left
        if self.maze_matrix[y][x] == 'O':
          return x,y
  def distCalc(self, position):
    goalX, goalY = self.findGoal()
    
    x, y = position
    dist = abs(goalX - x) + abs(goalY -y)
    return dist  
    



class State:
  def __init__(self,maze,pos):
    self.maze = maze
    self.position = pos
  def __hash__(self):
    return hash(self.position)
  def printString(self):
      print("Current Maze State:")
      print("Position: (",self.position,")")
      self.maze.printMaze(self.position)

class Problem:
  def __init__(self, initial):
    self.initialState = initial
  def actions(self, currentState):
    actions = ["up","down","left","right"]
    j,i = currentState.position
    if (Maze.get(currentState.maze,(j+1,i)) == 'X'):
      actions.remove("right")
    if (Maze.get(currentState.maze,(j-1,i)) == 'X'):
      actions.remove("left")
    if (Maze.get(currentState.maze,(j,i+1)) == 'X'):
      actions.remove("down")
    if (Maze.get(currentState.maze,(j,i-1)) == 'X'):
      actions.remove("up")
    return actions

  def takeAction(self,currentState,chosenAction):
    x,y = currentState.position
    if (chosenAction == "right"):
      returnPosition = (x+1,y)
    if (chosenAction == "left"):
      returnPosition = (x-1,y)
    if (chosenAction == "up"):
      returnPosition = (x,y-1)
    if (chosenAction == "down"):
      returnPosition = (x,y+1)
    return State(currentState.maze,returnPosition)

  def testForGoal(self,currentState):
    if (Maze.get(currentState.maze,currentState.position) == 'O'):
      return True
    else:
      return False

    
    

class Node:
  def __init__(self, state, parentNode = None, action = None, parentCost = 0):
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
    nextNode = Node(nextState, self, action, self.costToPresent +1)
    return nextNode
  def expand(self, problem):
    returnNodes = []
    for action in problem.actions(self.state):
      returnNodes.append(self.childNodes(problem,action))
    return returnNodes

def breadth_first_search(problem):
  node = Node(problem.initialState)
  if problem.testForGoal(node.state):
    return node
  mazeQueue = collections.deque([node])
  exploredStates = set()
  while mazeQueue:
    node = mazeQueue.popleft()
    exploredStates.add(node.state)
    for child in node.expand(problem):
      if child.state not in exploredStates and child not in mazeQueue:
        if problem.testForGoal(child.state):
          return child
        mazeQueue.append(child)
  return None

def printlist(pList):
  returnString = ""
  for entry in pList:
    returnString += "Node cost: " + str(entry.totalEstimation) + "\n"
  return returnString

def astarSearch(problem):
  node = Node(problem.initialState)
  exploredStates = set()
  PriorityQueueList = []
  PriorityQueueList.append(node)
  while PriorityQueueList:
    node = PriorityQueueList.pop(0)
    exploredStates.add(hash(node.state))
    if problem.testForGoal(node.state):
          return node
    for child in node.expand(problem):
      if (hash(child.state) not in exploredStates) and (child not in PriorityQueueList):
        PriorityQueueList.append(child)
      elif child in PriorityQueueList:
        index = PriorityQueueList.index(child)
        if child.totalEstimation < PriorityQueueList[index].totalEstimation:
          PriorityQueueList.remove(child)
          PriorityQueueList.append(child)
          PriorityQueueList = sorted(PriorityQueueList, key=lambda x: x.totalEstimation)
  return None
          

def printActions(finalNode):
  currentNode = finalNode
  actions = []
  actions.append(currentNode.action)
  while currentNode.parent:
    currentNode = currentNode.parent
    if (currentNode.action != None):
      actions.insert(0, currentNode.action)
  return actions

def printStates(Node):
  if Node.parent:
    printStates(Node.parent)
  if (Node.action != None):
    print("Action: ", Node.action)
    Node.state.printString()
  return 0



maze1 = """XXXXXXXXXXXXXXX
X.............X
X.............X
X......O......X
X.............X
X.............X
X.............X
XXXXXXXXXXXXXXX"""
# Important to remember: top left is (0,0)
# Y (or i) increases as it goes down
# X (or j) increases as it goes right
startingPosition = (1,1)
maze1_Init = Maze(maze1)
maze1_State = State(maze1_Init, startingPosition)
maze1_Problem = Problem(maze1_State)
Answer = astarSearch(maze1_Problem)

print(printActions(Answer))
printStates(Answer)