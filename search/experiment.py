def search_algorithm(problem, data_structure):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    #Initialise data structure 
    data_structure.push([(problem.getStartState(), "Start", 0)])
    states_visited = []

    while not data_structure.isEmpty():

        #Current state
        all_prev_states = data_structure.pop() #Path to current positon - all previous states
        position_current = all_prev_states[-1][0] #Current postion 

        #i. Check if the current postion is the goal
        if problem.isGoalState(position_current):
            #Return the actions executed to reach the goal state 
            actions_previous = [i[1] for i in all_prev_states]
            actions_previous = actions_previous[1:] #Discard starting state
            return actions_previous
        
        #ii. Check if the current state has been visited
        if position_current not in states_visited:
            #Append current state to visited 
            states_visited.append(position_current)

        #Inspect successors 
        successors = problem.getSuccessors(position_current)

        for successor in successors:
            position_successor = successor[0] #position of 
            action_successor = successor[1] #direction needed to take to get to position

            if position_successor not in visited:
                #Get path taken to reach this state
                path_successors = all_prev_states
                #Append the successor path 
                path_successors.append(successor)
                #Push to data structure
                data_structure.push(path_successors)

    #Return False if the search fails 
    return False


def search_algorithm2(problem, structure):
    """
    Defines a general algorithm to search a graph.
    Parameters are structure, which can be any data structure with .push() and .pop() methods, and problem, which is the
    search problem.
    """

    # Push the root node/start into the data structure in this format: [(state, action taken, cost)]
    # The list pushed into the structure for the second node will look something like this:
    # [(root_state, "Stop", 0), (new_state, "North", 1)]
    structure.push([(problem.getStartState(), "Stop", 0)])

    # Initialise the list of visited nodes to an empty list
    visited = []

    # While the structure is not empty, i.e. there are still elements to be searched,
    while not structure.isEmpty():
        # get the path returned by the data structure's .pop() method
        path = structure.pop()

        # The current state is the first element in the last tuple of the path
        # i.e. [(root_state, "Stop", 0), (new_state, "North", 1)][-1][0] = (new_state, "North", 1)[0] = new_state
        curr_state = path[-1][0]

        # if the current state is the goal state,
        if problem.isGoalState(curr_state):
            # return the actions to the goal state
            # which is the second element for each tuple in the path, ignoring the first "Stop"
            return [x[1] for x in path][1:]

        # if the current state has not been visited,
        if curr_state not in visited:
            # mark the current state as visited by appending to the visited list
            visited.append(curr_state)

            # for all the successors of the current state,
            for successor in problem.getSuccessors(curr_state):
                # successor[0] = (state, action, cost)[0] = state
                # if the successor's state is unvisited,
                if successor[0] not in visited:
                    # Copy the parent's path
                    successorPath = path[:]
                    # Set the path of the successor node to the parent's path + the successor node
                    successorPath.append(successor)
                    # Push the successor's path into the structure
                    structure.push(successorPath)

    # If search fails, return False
    return False