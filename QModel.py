import collections
import math
import random
from queue import PriorityQueue
import numpy as np



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

"""
=================================================================================================================================
Main
=================================================================================================================================
"""

# Important to remember: top left is (0,0)
# Y (or i) increases as it goes down
# X (or j) increases as it goes right
size = 15
mazeString, startingPosition, goalPosition, freeSpaces = createMaze(size)
print("Created Maze:")
for i in mazeString:
  print(i)
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
