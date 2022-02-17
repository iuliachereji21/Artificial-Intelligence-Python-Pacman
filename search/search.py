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

class Node:
    def __init__(self, state, parent, action, cost):
        self.state=state
        self.parent=parent
        self.action=action
        self.cost=cost
    def __eq__(self, other):
        if other == None: return False
        return self.state==other.state

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

    def expand(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (child,
        action, stepCost), where 'child' is a child to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that child.
        """
        util.raiseNotDefined()

    def getActions(self, state):
        """
          state: Search state

        For a given state, this should return a list of possible actions.
        """
        util.raiseNotDefined()

    def getActionCost(self, state, action, next_state):
        """
          state: Search state
          action: action taken at state.
          next_state: next Search state after taking action.

        For a given state, this should return the cost of the (s, a, s') transition.
        """
        util.raiseNotDefined()

    def getNextState(self, state, action):
        """
          state: Search state
          action: action taken at state

        For a given state, this should return the next state after taking action from state.
        """
        util.raiseNotDefined()

    def getCostOfActionSequence(self, actions):
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


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    frontier = util.Stack()
    frontier.push(Node(problem.getStartState(),None,None,0))
    expanded=[]
    while(not frontier.isEmpty()):
        currentNode=frontier.pop()
        if(problem.isGoalState(currentNode.state)):
            #if we reached the goal state start constructing the list of actions that got us here
            listToReturn=[]
            node1=currentNode
            while(node1.action!=None):
                listToReturn.insert(0,node1.action)
                node1=node1.parent
            return listToReturn
        if(currentNode not in expanded):
            expanded.append(currentNode)
            children=problem.expand(currentNode.state)
            #[frontier.push(Node(x[0],currentNode,x[1],x[2])) for x in children if ((Node(x[0],currentNode,x[1],x[2]) not in expanded) and (Node(x[0],currentNode,x[1],x[2]) not in frontier.list))]
            [frontier.push(Node(x[0], currentNode, x[1], x[2])) for x in children if (
                        (Node(x[0], currentNode, x[1], x[2]) not in expanded))]
            #we add the current node in the expanded list and add all its children (states we can get to from the current state to the frontier if they were not yet expanded
    return []

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    frontier = util.Queue()
    frontier.push(Node(problem.getStartState(), None, None, 0))
    expanded = []
    while (not frontier.isEmpty()):
        currentNode = frontier.pop()

        if (problem.isGoalState(currentNode.state)):
            listToReturn = []
            node1 = currentNode
            while (node1.action != None):
                listToReturn.insert(0, node1.action)
                node1 = node1.parent
            return listToReturn
        if (currentNode not in expanded):
            expanded.append(currentNode)
            children = problem.expand(currentNode.state)
            """[frontier.push(Node(x[0],currentNode,x[1],x[2])) for x in children if ((Node(x[0],currentNode,x[1],x[2]) not in expanded) and (Node(x[0],currentNode,x[1],x[2]) not in frontier.list))]"""
            [frontier.push(Node(x[0], currentNode, x[1], x[2])) for x in children if (
                (Node(x[0], currentNode, x[1], x[2]) not in expanded))]
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue()
    frontier.push(Node(problem.getStartState(), None, None, 0),heuristic(problem.getStartState(),problem))
    expanded = []
    while (not frontier.isEmpty()):
        currentNode = frontier.pop()
        if (problem.isGoalState(currentNode.state)):
            listToReturn = []
            node1 = currentNode
            while (node1.action != None):
                listToReturn.insert(0, node1.action)
                node1 = node1.parent
            return listToReturn
        if (currentNode not in expanded):
            expanded.append(currentNode)
            children = problem.expand(currentNode.state)
            """[frontier.push(Node(x[0],currentNode,x[1],x[2])) for x in children if ((Node(x[0],currentNode,x[1],x[2]) not in expanded) and (Node(x[0],currentNode,x[1],x[2]) not in frontier.list))]"""
            """[frontier.update(Node(x[0], currentNode, x[1], x[2] + currentNode.cost),) for x in children if (
                (Node(x[0], currentNode, x[1], x[2] + currentNode.cost) not in expanded))]"""

            for child in children:
                nod=Node(child[0],currentNode,child[1], child[2] + currentNode.cost)
                if nod not in expanded :
                    frontier.update(nod,nod.cost+heuristic(nod.state,problem))
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
