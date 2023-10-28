import collections

class Maze:
  def __init__(self,inputString):
    self.maze_matrix = []
    counter = 0
    for row in inputString.split('\n'):
      maze_row = []
      maze_row.extend(row)
      print("length of row:",len(maze_row))
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



class State:
  def __init__(self,maze,pos):
    self.maze = maze
    self.position = pos
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
    j,i = currentState.position
    if (chosenAction == "right"):
      returnPosition = (j+1,i)
    if (chosenAction == "left"):
      returnPosition = (j-1,i)
    if (chosenAction == "up"):
      returnPosition = (j,i-1)
    if (chosenAction == "down"):
      returnPosition = (j,i+1)
    return State(currentState.maze,returnPosition)

  def testForGoal(self,currentState):
    if (Maze.get(currentState.maze,currentState.position) == 'O'):
      return True
    else:
      return False

class Node:
  def __init__(self, state, parentNode = None, action = None, cost = 0):
    self.state = state
    self.parent = parentNode
    self.action = action
    self.pathCost = cost
    self.depth = 0
    if parentNode:
      self.depth = parentNode.depth + 1

  def childNodes(self, problem, action):
    nextState = problem.takeAction(self.state, action)
    nextNode = Node(nextState, self, action, (self.pathCost + 1)) #UPDATE LATER FOR ADJUSTING PATH COST
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

def printActions(finalNode):
  currentNode = finalNode
  actions = []
  actions.append(currentNode.action)
  while currentNode.parent:
    currentNode = currentNode.parent
    if (currentNode.action != None):
      actions.append(currentNode.action)
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
Answer = breadth_first_search(maze1_Problem)

print(printActions(Answer))
printStates(Answer)