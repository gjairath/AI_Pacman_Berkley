# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        #newSomething = successorGameState.getGhostPositions()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        #print('scared', newScaredTimes)
        "*** YOUR CODE HERE ***"
        someList = []
        foodVisited = []
        for x in newFood.asList():
            foodVisited.append(x)
            someList.append(manhattanDistance(x, newPos))
        
        distanceofGhost = manhattanDistance(newPos, newGhostStates[0].getPosition())
        foodEaten = []
        weight = successorGameState.getScore()
        for item in newFood.asList():
            if item not in someList:
                foodEaten.append(item)
        
        if (len(someList)):
            weight += 10 / min(someList)
        if (distanceofGhost):
            weight -= 10 / distanceofGhost
        if (newScaredTimes[0] != 0):
            weight += 1000 / (distanceofGhost+1) # play really agressive when ghost scared
            #pass
        if (len(foodEaten)):
            weight += 10 / len(foodEaten) #award for eating more
            #pass
        return weight

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    '''
    def maxVal(self, state, depth, agentI, action):
        v = -999999
        if depth == self.depth:
            return self.evaluationFunction(state)
        for action in state.getLegalActions(agentI):
                v = max(v, self.minVal(state.generateSuccessor(agentI, action), depth + 1, agentI, action))
        return v, action
    
    def minVal(self, state, depth, agentI, action):
        v = +999999
        if depth == self.depth:
            return self.evaluationFunction(state)
        for action in state.getLegalActions(agentI):
                v = max(v, self.maxVal(state.generateSuccessor(agentI, action), depth + 1, agentI, action))
        return v, action
    '''
    #When in doubt, blame the referenced code!
    
    def isTerminal(self, state, depth, agent):
        return depth == 0 or state.isWin() or state.isLose() or state.getLegalActions(agent) == 0
    
    def alphabeta(self, state, depth, agentI, action):
        
        if self.isTerminal(state, depth, agentI):
             return action, self.evaluationFunction(state)
        
        if agentI == 0:
            infValue = (-9999999.0, Directions.STOP)
            for action in state.getLegalActions(agentI):
                value = (self.alphabeta(state.generateSuccessor(agentI, action), depth - 1, agentI ,(action if depth is self.depth*state.getNumAgents() else action)))
                if value[0] > infValue[0]:
                    infValue = value
               # ac = action
            return infValue
        else:
            value = +999999.0
            for action in state.getLegalActions(agentI):
                value = min(value, self.alphabeta(state.generateSuccessor(agentI, action), depth - 1, agentI, (action if depth is self.depth*state.getNumAgents() else action)))
                
            return min(state.getLegalActions(agentI))
    
    def getAction(self, gameState):

        ac = self.alphabeta(gameState, self.depth*gameState.getNumAgents(), 0, 'Stop')
        return ac
        
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

