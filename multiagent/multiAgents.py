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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
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

        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        foodNow = currentGameState.getFood()
        foodNowList = foodNow.asList()
        "*** YOUR CODE HERE ***"
        """
        listFood=newFood.asList()
        distFood=-1
        lenListFood=len(listFood)
        for i in range(lenListFood):
            md=util.manhattanDistance(newPos,listFood[i])
            if distFood==-1:
                distFood=md
            else:
                if md<distFood:
                    distFood=md

        listGhosts=childGameState.getGhostPositions()
        distGhost = -1
        lenLisGhost = len(listGhosts)
        for i in range(lenLisGhost):
            mdg = util.manhattanDistance(newPos, listGhosts[i])
            if distGhost == -1:
                distGhost = mdg
            else:
                if mdg < distGhost:
                    distGhost = mdg

        if distGhost<=1: weightGhost=0
        else:
            if distGhost<=3: weightGhost=0.5
            else:
                if distGhost<=6: weightGhost=0.6
                else: weightGhost=0.7
        weightFood=1-weightGhost
        
        return weightGhost*distGhost - weightFood*distFood"""
        """I tried to calculate the minimum distance between pacman and each food and the min dist between pacman and each 
        ghost and use weights but if the ghost does not come to pacman it does not behave well and does not go to the food"""

        "return childGameState.getScore()"

        for ghost in newGhostStates:
            if ghost.getPosition() == tuple(newPos) and (ghost.scaredTimer == 0):
                return -10000000

        maxDist = -10000000
        for food in foodNowList:
            dist = util.manhattanDistance(newPos, food) * -1
            if (dist > maxDist):
                maxDist = dist

        return maxDist

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

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        def miniMax(gameState, howDeep, agent):
            if agent >= gameState.getNumAgents():
                #we completed new level in the tree (pacman and all the ghosts), so we increase depth and start over with pacman (agent 0)
                agent = 0
                howDeep = howDeep + 1
            if (gameState.isWin() or gameState.isLose() or howDeep == self.depth):
                #we reached a terminal leaf (win or lost) that can't be expanded no more or we reached the maximum depth given to the problem
                #so we take no more actions and return the current state's score
                return {"action":"none", "value":self.evaluationFunction(gameState)}
            else:
                #we expand further
                if (agent == 0):
                    #it is pacman's turn so we use the maxHelper function
                    return maxHelper(gameState, howDeep, agent)
                else:
                    #it is a ghost's turn so we use the miniHelper function#
                    return miniHelper(gameState, howDeep, agent)

        def maxHelper(gameState, howDeep, agent):
            pacmanActions = gameState.getLegalActions(agent)
            if len(pacmanActions)==0:
                #there are no more actions that can be made from this state so we return the state's score
                return {"action":"none", "value":self.evaluationFunction(gameState)}

            output={"action":"none", "value":-10000000}
            for action in pacmanActions:
                #expand the tree starting from each of the next actions, for the other agents (ghosts), and the deepness does not change
                nextState = gameState.getNextState(agent, action)
                currentValue = miniMax(nextState, howDeep, agent + 1)
                #since we are on pacman's turn (max), we choose the greatest value of the possibilities and return it together with the action that
                #takes us there
                if currentValue["value"]>output["value"]:
                    output["action"]=action
                    output["value"]=currentValue["value"]
            return output

        def miniHelper(gameState, howDeep, agent):
            ghostActions = gameState.getLegalActions(agent)
            if len(ghostActions)==0:
                #there are no more actions that can be made from this state so we return the state's score
                return {"action":"none", "value":self.evaluationFunction(gameState)}

            output = {"action": "none", "value": 10000000}
            for action in ghostActions:
                #expand the tree starting from each of the next actions, for the other agents (the remaining ghosts), and the deepness does not change
                nextState = gameState.getNextState(agent, action)
                currentValue = miniMax(nextState, howDeep, agent + 1)
                #since we are on a ghost's turn (mini), we choose the smallest value of the possibilities and return it together with the action that
                #takes us there
                if currentValue["value"]<output["value"]:
                    output["action"]=action
                    output["value"]=currentValue["value"]
            return output

        outputFinal=miniMax(gameState, 0, 0)
        return outputFinal["action"]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def miniMax(gameState, howDeep, agent, maximum, minimum):
            if agent >= gameState.getNumAgents():
                #we completed new level in the tree (pacman and all the ghosts), so we increase depth and start over with pacman (agent 0)
                agent = 0
                howDeep = howDeep + 1
            if (gameState.isWin() or gameState.isLose() or howDeep == self.depth):
                #we reached a terminal leaf (win or lost) that can't be expanded no more or we reached the maximum depth given to the problem
                #so we take no more actions and return the current state's score
                return {"action": "none", "value": self.evaluationFunction(gameState)}
            else:
                #we expand further
                if (agent == 0):
                    #it is pacman's turn so we use the maxHelper function
                    return maxHelper(gameState, howDeep, agent, maximum, minimum)
                else:
                    #it is a ghost's turn so we use the miniHelper function
                    return miniHelper(gameState, howDeep, agent, maximum, minimum)

        def maxHelper(gameState, howDeep, agent, maximum, minimum):
            pacmanActions = gameState.getLegalActions(agent)
            if len(pacmanActions) == 0:
                #there are no more actions that can be made from this state so we return the state's score
                return {"action": "none", "value": self.evaluationFunction(gameState)}

            "initialize v as minus infinity"
            output = {"action": "none", "value": -10000000}
            for action in pacmanActions:
                #expand the tree starting from each of the next actions, for the other agents (ghosts), and the deepness does not change
                nextState = gameState.getNextState(agent, action)
                currentValue = miniMax(nextState, howDeep, agent + 1, maximum, minimum)
                #since we are on pacman's turn (max), we choose the greatest value of the possibilities and return it together with the action that
                #takes us there
                "v=max(v, value(successor,alpha, beta))"
                if currentValue["value"] > output["value"]:
                    output["action"] = action
                    output["value"] = currentValue["value"]

                #if the current value from this subtree is greater than the so far minimum (possibly from another branch) then we don't need
                #to expand the other subtrees because this means that this whole branch will not be chosen for the solution so it is an optimization
                #to return here and to not work further in vain
                "if v>beta return v"
                if output["value"]>minimum:
                    return output

                #else if the current value is greater than the so far maximum then the maximum gets the value of the current value
                "alpha = max(alpha,v)"
                if output["value"]>maximum:
                    maximum=output["value"]

            return output

        def miniHelper(gameState, howDeep, agent, maximum, minimum):
            ghostActions = gameState.getLegalActions(agent)
            if len(ghostActions) == 0:
                #there are no more actions that can be made from this state so we return the state's score
                return {"action": "none", "value": self.evaluationFunction(gameState)}

            "initialize v as infinity"
            output = {"action": "none", "value": 10000000}
            for action in ghostActions:
                #expand the tree starting from each of the next actions, for the other agents (the remaining ghosts), and the deepness does not change
                nextState = gameState.getNextState(agent, action)
                currentValue = miniMax(nextState, howDeep, agent + 1, maximum, minimum)
                #since we are on a ghost's turn (mini), we choose the smallest value of the possibilities and return it together with the action that
                #takes us there
                "v=min(v, value(successor,alpha, beta))"
                if currentValue["value"] < output["value"]:
                    output["action"] = action
                    output["value"] = currentValue["value"]

                #if the current value from this subtree is smaller than the so far maximum (possibly from another branch) then we don't need to
                #expand the other subtrees because this means that this whole branch will not be chosen for the solution so it is an optimization
                #to return here and to not work further in vain
                "if v<alpha return v"
                if output["value"]<maximum:
                    return output

                #else if the current value is smaller than the so far minimum then the minimum gets the value of the current value
                "beta = min(beta,v)"
                if output["value"]<minimum:
                    minimum=output["value"]

            return output

        outputFinal = miniMax(gameState, 0, 0, -10000000, 10000000)
        return outputFinal["action"]

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
