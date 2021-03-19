# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


#***************************************
#SOLUTION: PART 1.SEARCH - Q1-4 

#USED IN Q1-4
#A General graph search algorithm 
def search_algorithm(problem, data_structure):
    """
    A general graph search algorithm for pacman that can be used to execute dfs, bfs, ucs and a* depending on the given data structure used
    The algorithm returns a list of actions that reaches the goal. 
    
    Paramaters
    - problem
    - data_structure: The data structure, a stack for dfs, a queue for bfs, and a priority queue for ucs and a*

    Returns:
    - actions_goal: A list of actions that reaches the  goal
    """

    #Initialise data structure 
    data_structure.push([(problem.getStartState(), "Start", 0)])
    states_visited = []

    while data_structure.isEmpty() == 0:

        #Current state
        all_prev_states = data_structure.pop() #Path to current positon - all previous states
        position_current = all_prev_states[-1][0] #Current postion 

        #i. Check if the current postion is the goal
        if problem.isGoalState(position_current):
            #Return the actions executed to reach the goal state 
            actions_goal = [i[1] for i in all_prev_states]
            actions_goal = actions_goal[1:] #Discard starting action 
            return actions_goal
        
        #ii. Check if the current state has been visited
        if position_current not in states_visited:
            #Append current state to visited 
            states_visited.append(position_current)

            #iii. Inspect successors of current state to determine next step to take
            for state_next in problem.getSuccessors(position_current):
                position_next = state_next[0] #position of 
        
                if position_next not in states_visited:
                    #Get path taken to reach this state
                    path = all_prev_states[:]
                    #Append the successor path 
                    path.append(state_next)
                    #Push to data structure
                    data_structure.push(path)

    #Return False if the search fails 
    return False

#*************************
#Q1 DEPTH FIRST SEARCH

def depthFirstSearch(problem):

    """Implementation of depth First search - searches the deepest nodes in the search tree first.
    The method search_algorithm is used which is a general graph search algorithm for pacaman.
    A stack is the data structure used in depthFirstSearch and passed to search_algorithm  

    Returns:
    - actions_goal: A list of actions that reaches the  goal
    """
    
    #Initialize a stack
    stack = util.Stack()
    actions_goal = search_algorithm(problem, stack)

    return actions_goal

#*************************
#Q2 BREATH FIRST SEARCH

def breadthFirstSearch(problem):

    """Implementation of breath First search - searches the shallowest nodes in the search tree first.
    The method search_algorithm is used which is a general graph search algorithm for pacaman.
    A stack is the data structure used in breadthFirstSearch and passed to search_algorithm  

    Returns:
    - actions_goal: A list of actions that reaches the goal
    """
    
    #Initialize a queue 
    queue = util.Queue()
    actions_goal = search_algorithm(problem, queue)

    return actions_goal

#****************************
#Q3.UNIFORM COST SEARCH
def get_uni_cost(problem):
    """Function which returns cost of the path in the form of a function object to be used by PriorityQueueWithFunction """

    #Function object to be used by PriorityQueueWithFunction
    function_object = lambda states: problem.getCostOfActions([state[1] for state in states][1:])

    return function_object

def uniformCostSearch(problem):

    """ Graph search algorithm which searches the node of least total cost first.
    The method search_algorithm is used in conjunction with a priority queue which sorts by the cost"""

    #Initialise priority queue using PriorityQueueWithFunction which takes a priority function
    priority_queue = util.PriorityQueueWithFunction(get_uni_cost(problem))
    actions_goal = search_algorithm(problem, priority_queue)

    return actions_goal

#*****************
#Q4 A STAR SEARCH

def get_astar_cost(problem, heuristic):

    """Function which returns cost of the path in the form of a function object to be used by PriorityQueueWithFunction
    The specific cost in a* search is:f(x) = g(x) + h(x).
    Whereby g(x) is the backward cost and h(x) is the heuristic """

    #Function object to be used by PriorityQueueWithFunction
    function_object = lambda states: problem.getCostOfActions([state[1] for state in states][1:]) + heuristic(states[-1][0], problem)

    return function_object

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):

    """ Search the node that has the lowest combined cost and heuristic first.
    The method search_algorithm is used in conjunction with a priority queue which sorts by the a star cost"""

    #Initialise priority queue using PriorityQueueWithFunction which takes a priority function
    priority_queue = util.PriorityQueueWithFunction(get_astar_cost(problem, heuristic))
    actions_goal = search_algorithm(problem, priority_queue)

    return actions_goal


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
