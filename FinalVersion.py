# -*- coding: utf-8 -*-
"""MLSearcher.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rWTj_xgLiOqoUosAGrf6EPyOxySyNpdi
"""

import collections
import math
import random
from queue import PriorityQueue
import numpy as np

"""
=================================================================================================================================
BFS and A*
=================================================================================================================================
"""

class Maze:
  def __init__(self,inputString, startPos):
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
          if startPos == [i,j]:

            row.append("+")
          else:
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
      print("Position:",self.position)
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
    exploredStates.add(hash(node.state))
    for child in node.expand(problem):
      if hash(child.state) not in exploredStates and child not in mazeQueue:
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






"""
=================================================================================================================================
Q-Learning Algorithm
=================================================================================================================================
"""


def createRewardMap(maze):
  rewardMap = []
  for y in range(len(maze)):
    mazeString = []
    for x in range(len(maze[0])):
      if (maze[y][x] == 'X'):
        mazeString.append(-100)
      if (maze[y][x] == '.'):
        mazeString.append(-1)
      if (maze[y][x] == 'O'):
        mazeString.append(100)
    rewardMap.append(mazeString)
  return rewardMap

class QLearningModel:
  def __init__(self, rewardMap, inMaze, startPos, inQ, inSpaces):
    self.reward = rewardMap
    self.maze = inMaze
    self.start = startPos
    self.QMatrix = inQ
    self.options = ["up","down","left","right"]
    self.freeSpaces = inSpaces
  def randoStart(self):
    return random.choice(self.freeSpaces)
  def wallCollision(self, y, x):
    if self.reward[y][x] != -1:
      return True
    else:
      return False
  def chooseAction(self, y, x, eps):
    if np.random.random() < eps:
      return np.argmax(self.QMatrix[y,x])
    else: #choose a random action
      return np.random.randint(4)
  def moveDrone(self, currentY, currentX, action):
    if (self.options[action] == "right"):
      currentX += 1
    if (self.options[action] == "left"):
      currentX -= 1
    if (self.options[action] == "up"):
      currentY -= 1
    if (self.options[action] == "down"):
      currentY += 1
    return currentY, currentX
  def shortestPath(self, inY, inX):
    if self.wallCollision(inY, inX):
      return []
    else:
      y, x = inY, inX
      path = []
      path.append([y,x])
      while not self.wallCollision(y,x):
        Action = self.chooseAction(y,x,1.)
        y, x = self.moveDrone(y,x,Action)
        path.append([y,x])
      return path
"""
=================================================================================================================================
Creation of Randomly Generated Mazes
=================================================================================================================================
"""


def checkNeighbor(mazeString, coordinates):
  freeSpaces = 0
  if (mazeString[coordinates[0]-1][coordinates[1]] == '.'):
    freeSpaces += 1
  if (mazeString[coordinates[0]+1][coordinates[1]] == '.'):
    freeSpaces += 1
  if (mazeString[coordinates[0]][coordinates[1]-1] == '.'):
    freeSpaces += 1
  if (mazeString[coordinates[0]][coordinates[1]+1] == '.'):
    freeSpaces += 1
  return freeSpaces

def createMaze(size):
  mazeString = []
  borderLine = ""
  #Creates a blank maze
  for i in range(0,size):
    line = []
    for j in range(0,size):
      line.append('=')
    mazeString.append(line)

  #Pick random starting position in maze
  startY = int(random.random()*size)
  startX = int(random.random()*size)
  #Ensures position is not on an edge
  if startX == 0:
    startX += 1
  if startX == size-1:
    startX -= 1
  if startY == 0:
    startY += 1
  if startY == size-1:
    startY -= 1

  #Randomly selecting walls
  walls = []
  mazeString[startY][startX] = '.'
  walls.append([startY-1,startX])
  mazeString[startY-1][startX] = 'X'
  walls.append([startY+1,startX])
  mazeString[startY+1][startX] = 'X'
  walls.append([startY,startX-1])
  mazeString[startY][startX-1] = 'X'
  walls.append([startY,startX+1])
  mazeString[startY][startX+1] = 'X'

  #Remember [y,x] [0,1]
  while walls:
    randWall = walls[int(random.random()*len(walls))-1]
    #Checking for X. (LEFT WALL)
    if randWall[1] != '.':
      if mazeString[randWall[0]][randWall[1]-1] == '=' and mazeString[randWall[0]][randWall[1]+1] == '.':
        free = checkNeighbor(mazeString,randWall)
        if free < 2:
          mazeString[randWall[0]][randWall[1]] = '.'
          #Upper
          if (randWall[0] != 0):
            if (mazeString[randWall[0]-1][randWall[1]] != '.'):
              mazeString[randWall[0]-1][randWall[1]] = 'X'
            if (mazeString[randWall[0]-1][randWall[1]] not in walls):
              walls.append([randWall[0]-1, randWall[1]])
          #Bottom
          if (randWall[0] != size-1):
            if (mazeString[randWall[0]+1][randWall[1]] != '.'):
              mazeString[randWall[0]+1][randWall[1]] = 'X'
            if (mazeString[randWall[0]+1][randWall[1]] not in walls):
              walls.append([randWall[0]+1, randWall[1]])
          #Left
          if (randWall[1] != 0):
            if (mazeString[randWall[0]][randWall[1]-1] != '.'):
              mazeString[randWall[0]][randWall[1]-1] = 'X'
            if (mazeString[randWall[0]][randWall[1]-1] not in walls):
              walls.append([randWall[0], randWall[1]-1])
        for wall in walls:
          if (wall[0] == randWall[0] and wall[1] == randWall[1]):
            walls.remove(wall)
        continue
    #Checking for .X (RIGHT WALL)
    if randWall[1] != size-1:
      if mazeString[randWall[0]][randWall[1]-1] == '.' and mazeString[randWall[0]][randWall[1]+1] == '=':
        free = checkNeighbor(mazeString,randWall)
        if free < 2:
          mazeString[randWall[0]][randWall[1]] = '.'
          #Upper
          if (randWall[0] != 0):
            if (mazeString[randWall[0]-1][randWall[1]] != '.'):
              mazeString[randWall[0]-1][randWall[1]] = 'X'
            if (mazeString[randWall[0]-1][randWall[1]] not in walls):
              walls.append([randWall[0]-1, randWall[1]])
          #Bottom
          if (randWall[0] != size-1):
            if (mazeString[randWall[0]+1][randWall[1]] != '.'):
              mazeString[randWall[0]+1][randWall[1]] = 'X'
            if (mazeString[randWall[0]+1][randWall[1]] not in walls):
              walls.append([randWall[0]+1, randWall[1]])
          #Right
          if (randWall[1] != size-1):
            if (mazeString[randWall[0]][randWall[1]+1] != '.'):
              mazeString[randWall[0]][randWall[1]+1] = 'X'
            if (mazeString[randWall[0]][randWall[1]+1] not in walls):
              walls.append([randWall[0], randWall[1]+1])
        for wall in walls:
          if (wall[0] == randWall[0] and wall[1] == randWall[1]):
            walls.remove(wall)
        continue
    #Checking for ./X (TOP WALL)
    if randWall[0] != 0:
      if mazeString[randWall[0]-1][randWall[1]] == '=' and mazeString[randWall[0]+1][randWall[1]] == '.':
        free = checkNeighbor(mazeString,randWall)
        if free < 2:
          mazeString[randWall[0]][randWall[1]] = '.'
          #Upper
          if (randWall[0] != 0):
            if (mazeString[randWall[0]-1][randWall[1]] != '.'):
              mazeString[randWall[0]-1][randWall[1]] = 'X'
            if (mazeString[randWall[0]-1][randWall[1]] not in walls):
              walls.append([randWall[0]-1, randWall[1]])
          #Right
          if (randWall[1] != size-1):
            if (mazeString[randWall[0]][randWall[1]+1] != '.'):
              mazeString[randWall[0]][randWall[1]+1] = 'X'
            if (mazeString[randWall[0]][randWall[1]+1] not in walls):
              walls.append([randWall[0], randWall[1]+1])
          #Left
          if (randWall[1] != 0):
            if (mazeString[randWall[0]][randWall[1]-1] != '.'):
              mazeString[randWall[0]][randWall[1]-1] = 'X'
            if (mazeString[randWall[0]][randWall[1]-1] not in walls):
              walls.append([randWall[0], randWall[1]-1])
        for wall in walls:
          if (wall[0] == randWall[0] and wall[1] == randWall[1]):
            walls.remove(wall)
        continue
    #Checking for X/. (BOTTOM WALL)
    if randWall[0] != size-1:
      if mazeString[randWall[0]-1][randWall[1]] == '.' and mazeString[randWall[0]+1][randWall[1]] == '=':
        free = checkNeighbor(mazeString,randWall)
        if free < 2:
          mazeString[randWall[0]][randWall[1]] = '.'
          #Bottom
          if (randWall[0] != size-1):
            if (mazeString[randWall[0]+1][randWall[1]] != '.'):
              mazeString[randWall[0]+1][randWall[1]] = 'X'
            if (mazeString[randWall[0]+1][randWall[1]] not in walls):
              walls.append([randWall[0]+1, randWall[1]])
          #Right
          if (randWall[1] != size-1):
            if (mazeString[randWall[0]][randWall[1]+1] != '.'):
              mazeString[randWall[0]][randWall[1]+1] = 'X'
            if (mazeString[randWall[0]][randWall[1]+1] not in walls):
              walls.append([randWall[0], randWall[1]+1])
          #Left
          if (randWall[1] != 0):
            if (mazeString[randWall[0]][randWall[1]-1] != '.'):
              mazeString[randWall[0]][randWall[1]-1] = 'X'
            if (mazeString[randWall[0]][randWall[1]-1] not in walls):
              walls.append([randWall[0], randWall[1]-1])
        for wall in walls:
          if (wall[0] == randWall[0] and wall[1] == randWall[1]):
            walls.remove(wall)
        continue
    for wall in walls:
      if (wall[0] == randWall[0] and wall[1] == randWall[1]):
        walls.remove(wall)
   #Sets unvisited spaces to walls
  for i in range(0,size):
    for j in range(0,size):
      if (mazeString[i][j] == '='):
        mazeString[i][j] = 'X'
  # Randomly set the goal and starting state:
  freeSpaces = []
  for i in range(0,size):
    for j in range(0,size):
      if (mazeString[i][j] == '.'):
        freeSpaces.append([i,j])
  goalCord = random.choice(freeSpaces)
  freeSpaces.remove(goalCord)
  mazeString[goalCord[0]][goalCord[1]] = 'O'
  startCord = random.choice(freeSpaces)
  #Returns the Maze
  return mazeString, startCord, goalCord, freeSpaces

size = 15
mazeString, startingPosition, goalPosition, freeSpaces = createMaze(size)

string = ""
for row in range(0,len(mazeString)):
  for column in range(0, len(mazeString[row])):
    string += mazeString[row][column]
  string += '\n'
print(string)

y, x = startingPosition
pos2 = (x,y)

"""
=================================================================================================================================
Main - BFS Algorithm
=================================================================================================================================
"""
maze_Init = Maze(string, startingPosition)
maze_State = State(maze_Init, pos2)
maze_Problem = Problem(maze_State)
Answer1 = breadth_first_search(maze_Problem)
if (Answer1 != None):
  print("Results from BFS")
  print(printActions(Answer1))
  printStates(Answer1)
else:
  print("Drone unable to navigate via BFS to goal, make sure area connects to goal.")

"""
=================================================================================================================================
Main - A* Algorithm
=================================================================================================================================
"""
maze_Init = Maze(string, startingPosition)
maze_State = State(maze_Init, pos2)
maze_Problem = Problem(maze_State)
Answer2 = astarSearch(maze_Problem)
if (Answer2 != None):
  print("Results from A*")
  print(printActions(Answer2))
  printStates(Answer2)
else:
  print("Drone unable to navigate via A* to goal, make sure area connects to goal.")

"""
=================================================================================================================================
Main - Q-Learning Model
=================================================================================================================================
"""

# Important to remember: top left is (0,0)
# Y (or i) increases as it goes down
# X (or j) increases as it goes right

for row in range(0,len(mazeString)):
    string = []
    for column in range(0, len(mazeString[row])):
      if startingPosition == [row,column]:
        string.append("+")
      else:
        string.append(mazeString[row][column])
    print(string)
print("==================================================================")
rewardMap = createRewardMap(mazeString)

qMap = np.zeros((size,size,4))

# Training Model
runObj = QLearningModel(rewardMap,mazeString,startingPosition,qMap, freeSpaces)
for epoch in range(1000):
  y, x = runObj.randoStart()
  while not runObj.wallCollision(y,x):
    action = runObj.chooseAction(y, x, 0.9)
    oldY, oldX = y, x
    y, x = runObj.moveDrone(y,x,action)
    reward = runObj.reward[y][x]
    oldQ = runObj.QMatrix[oldY, oldX, action]
    temp = reward + (0.9 * np.max(runObj.QMatrix[y, x])) - oldQ
    runObj.QMatrix[oldY, oldX, action] = oldQ + (0.9 * temp)

# Testing Model
testY, testX = startingPosition
path = runObj.shortestPath(testY, testX)
Actions = []
previous = None
for pos in path:
  if previous != None:
    i, j = pos
    y, x = previous
    if y+1 == i:
      Actions.append('down')
    if y-1 == i:
      Actions.append('up')
    if x+1 == j:
      Actions.append('right')
    if x-1 == j:
      Actions.append('left')
  previous = pos
print("Solution:")
print(Actions)
print("==================================================================")
for pos in path:
  for row in range(0,len(mazeString)):
    string = []
    for column in range(0, len(mazeString[row])):
      if pos == [row,column]:
        string.append("+")
      else:
        string.append(mazeString[row][column])
    print(string)
  print(pos)
  print("==================================================================")