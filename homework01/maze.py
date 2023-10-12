from search import Problem

"""Basic class for representing a maze.
  Each maze cell is one of the following:
  . is an empty cell
  x is a goal
  # is a wall
  o is a teleporter (there are exactly two teleporter locations, or none)
"""
class Maze:
    def __init__(self,maze_string,maze_size):
        """define the maze using a string, and the maze width and height"""
        # remove whitespace
        width,height = maze_size
        maze_string = "".join(maze_string.split())
        assert len(maze_string) == width*height
        self.matrix = self._string_to_matrix(maze_string,maze_size)
        self.maze_size = maze_size

        self.teleporters = [ i for i,c in enumerate(maze_string) if c == 'o' ]
        self.teleporters = [ (i//width,i%width) for i in self.teleporters ]

        self.goals = [ i for i,c in enumerate(maze_string) if c == 'x' ]
        self.goals = [ (i//width,i%width) for i in self.goals ]

        assert len(self.teleporters) == 0 or len(self.teleporters) == 2

    def __repr__(self,position=None):
        if position is not None:
            x,y = position
            marker = self.matrix[x][y]
            self.matrix[x][y] = '+'
        # draw maze as string
        st = "\n".join( "".join(row) for row in self.matrix )
        # restore marker
        if position is not None:
            self.matrix[x][y] = marker
        return st

    def at(self,position):
        """returns the symbol at the maze location position=(x,y)"""
        x,y = position
        return self.matrix[x][y]

    def cleared_goals(self):
        """returns a copy of the maze without any goals"""
        maze_string = self.maze_string.replace('x','.')
        maze = Maze(maze_string,self.maze_size)

    def _string_to_matrix(self,string,size):
        w,h = size
        """convert string into a character matrix of width w and height h"""
        # turn the string into an array of rows
        # where each row is a sub-string
        mat = [ string[i*w:(i+1)*w] for i in range(h) ]
        # break each row into an array
        mat = [ list(row) for row in mat ]
        return mat

"""This class keeps track of a maze, and a player's position inside of
the maze.  When the state is printed, the player's position is denoted
with a + character"""
class MazeState:
    def __init__(self,maze,position):
        self.maze = maze
        self.position = position

    def __repr__(self):
        return self.maze.__repr__(position=self.position)

    def __lt__(self,other):
        return self.position < other.position

    def __eq__(self, other):
        return self.position == other.position

    def __hash__(self):
        return hash(self.position)

"""This class defines a maze problem."""
class MazeProblem(Problem):
    def __init__(self, initial):
        """A problem is initialized by its initial state.
        This function does not need to be modified."""
        super().__init__(initial)

    def actions(self, state):
        """Give a maze state, we need to return a list of valid actions"""
        
        # we have five possible actions, and we need to reduce these
        # possibilities depending on the player's current position
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT', 'TELEPORT']
        x,y = state.position

        # we need to move any possible action that is
        # invalid based on the current state of the maze
        if (Maze.at(state.maze,(x,y)) != 'o'):
            possible_actions.remove('TELEPORT')
        if (Maze.at(state.maze,(x,y-1)) == '#'):
            possible_actions.remove('LEFT')
        if (Maze.at(state.maze,(x,y+1)) == '#'):
            possible_actions.remove('RIGHT')
        if (Maze.at(state.maze,(x+1,y)) == '#'):
            possible_actions.remove('DOWN')
        if (Maze.at(state.maze,(x-1,y)) == '#'):
            possible_actions.remove('UP')
        # YOUR CODE HERE
        #raise Exception("IMPLEMENT THIS FUNCTION") # comment this out

        return possible_actions

    def result(self, state, action):
        """Given a maze state and a valid action, return the resulting 
        state found by applying the action"""
        x,y = state.position

        if (action == 'TELEPORT'):
            
            #print(state.position)
            #print(x,y)
            #print(state.maze.teleporters[0])
            if(state.maze.teleporters[0] == state.position):
                new_position = state.maze.teleporters[1]

            elif(state.maze.teleporters[1] == state.position):
                new_position = state.maze.teleporters[0]

        if (action == 'RIGHT'):
            new_position = (x,y+1)

        if (action == 'LEFT'):
            new_position = (x,y-1)

        if (action == 'UP'):
            new_position = (x-1,y)

        if (action == 'DOWN'):
            new_position = (x+1,y)


        # YOUR CODE HERE
        #raise Exception("IMPLEMENT THIS FUNCTION") # comment this out
        #print(state.maze)
        return MazeState(state.maze,new_position)

    def goal_test(self, state):
        """Return true if the given state is a goal state and return 
        false otherwise"""
        if(Maze.at(state.maze,state.position) == 'x'):
            return True
        else:
            return False
        # YOUR CODE HERE
        #raise Exception("IMPLEMENT THIS FUNCTION") # comment this out

        pass
