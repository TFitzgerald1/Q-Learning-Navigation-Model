#from search import breadth_first_graph_search as Searcher
from search import iterative_deepening_search as Searcher
from maze import *

def print_solution(solution):
    # given a solution path, print each state of the path
    path_actions = solution.solution()
    path_states = solution.path()
    print("====================")
    print(path_states[0].state)
    print("====================")
    for node,action in zip(path_states[1:],path_actions):
        print(action)
        print(node.state)
        print("====================")

def run_test(maze,starting_position,expected_cost):
    state = MazeState(maze,starting_position)
    problem = MazeProblem(state)
    searcher = Searcher(problem)

    print("maze:")
    print(state)
    print("solution:")
    print(searcher.solution())
    print_solution(searcher)
    print("cost: %d (expected %d)" % (searcher.path_cost,expected_cost) )
    if searcher.path_cost != expected_cost:
        print("==== TEST FAILED ====")
        return 0

    return 1

# count how many tests pass
passed = 0
total = 4



print("""
########################################
# TEST 1
########################################
""")
maze_string = """
#######
#.....#
#.....#
#.....#
#.....#
#....x#
#######
"""
maze = Maze(maze_string,(7,7))
starting_position = (1,1)
expected_cost = 8
passed += run_test(maze,starting_position,expected_cost)

print("""
########################################
# TEST 2
########################################
""")
maze_string = """
#######
#.....#
#....o#
#######
#....o#
#x....#
#######
"""
maze = Maze(maze_string,(7,7))
starting_position = (1,1)
expected_cost = 11
passed += run_test(maze,starting_position,expected_cost)

print("""
########################################
# TEST 3
########################################
""")
maze_string = """
###############
#...........#o# 
#####.#.#####.#
#.....#....o#.#
#.#####.#####.#
#.....#.....#x#
###############
"""
maze = Maze(maze_string,(15,7))
starting_position = (1,1)
expected_cost = 17
passed += run_test(maze,starting_position,expected_cost)

print("""
########################################
# TEST 4
########################################
""")
maze_string = """
###########
#x.......x#
#.........#
#.........#
#.........#
#o.......o#
#.........#
#.........#
#.........#
#x.......x#
###########
"""
maze = Maze(maze_string,(11,11))
starting_position = (5,5)
expected_cost = 8
passed += run_test(maze,starting_position,expected_cost)

print("====")
print("%d/%d TESTS PASSED" % (passed,total))
