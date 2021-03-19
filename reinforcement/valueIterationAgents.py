# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent

#*******************************************************
# QUESTION 1 - VALUE ITERATION

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        #Loop through iterations
        for iterX in range(self.iterations):
            values_temp = self.values.copy()
            states = self.mdp.getStates()

            #Iterate over states
            for state in states:

                #Check if not in final state
                if not mdp.isTerminal(state):
                    max_value = float("-inf") 
                
                    #Iterate over actions within the states
                    for action in mdp.getPossibleActions(state):
                        value = 0 

                        #Iterate over transition probabilities for a given action
                        for transition in mdp.getTransitionStatesAndProbs(state, action):
                            #print("transition[0] = {}".format(transition[0])) #State
                            #print("transition[1] = {}".format(transition[1])) #Probability 
                            updated_value = transition[1]*( mdp.getReward(state, action, transition[0]) + discount*self.values[transition[0]])
                            value = value + updated_value

                        #All transition probabilites for one action 
                        #Replace max value with current value if it is greater
                        if value > max_value:
                            max_value = value
                    
                    values_temp[state] = max_value

                #Else if in terminal state
                else:
                    for action in mdp.getPossibleActions(state):
                        value = 0
                        for transition in mdp.getTransitionStatesAndProbs(state, action):
                            updated_value = transition[1]*(mdp.getReward(state, action, transition[0]) + discount*self.values[transition[0]])
                            value = value + updated_value
                        
                        #Update values
                        values_temp[state] = value
            #Save values
            self.values = values_temp        


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        q_value = 0

        #Determine q value using the transition probabilities
        transitions = self.mdp.getTransitionStatesAndProbs(state, action)
        for transition in transitions:
            updated_q_value = transition[1]*(self.mdp.getReward(state, action, transition[0]) + self.discount*self.values[transition[0]])
            q_value = q_value + updated_q_value

        return q_value

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        actions = self.mdp.getPossibleActions(state)

        #Check it's not a terminal state
        if not self.mdp.isTerminal(state): 

            optimal_action = actions[0]
            optimal_q = self.getQValue(state, optimal_action)

            for action in self.mdp.getPossibleActions(state):

                if self.getQValue(state, action) > optimal_q:
                    optimal_action = action
                    optimal_q = self.getQValue(state, action)
        
            return optimal_action

        

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
