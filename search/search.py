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
from game import Directions
from typing import List


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


def tinyMazeSearch(problem: SearchProblem) -> List[Directions]:
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    start_state = problem.getStartState()
    frontier = [start_state]
    list_of_actions = []
    closed_set = []
    predecessor_map = {}

    while frontier:
        node = frontier.pop()  # pop last in
        if node == start_state:
            state = node
        else:
            state = node[0]

        if problem.isGoalState(state):
            temp_node = node

            list_of_actions.append(temp_node[1])  # last state
            while start_state != predecessor_map[temp_node]:
                list_of_actions.append(predecessor_map[temp_node][1])

                temp_node = predecessor_map[temp_node]

            list_of_actions.reverse()
            return list_of_actions

        if not state in closed_set:
            closed_set.append(state)

            for succcessor in problem.getSuccessors(state):
                predecessor_map[succcessor] = node
                frontier.append(succcessor)

   # util.raiseNotDefined()


def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    start_state = problem.getStartState()
    frontier = util.Queue()
    list_of_actions = []
    frontier.push((start_state, list_of_actions))  # with list of actions
    closed_set = []
    # predecessor_map = {}

    while not frontier.isEmpty():
        node = frontier.pop()  # pop first in queue
        state = node[0]
        # if node == start_state:
        #    state = node
        # else:
        #    state = node[0]

        if problem.isGoalState(state):
            # temp_node = node
            # list_of_actions.append(temp_node[1])  # last state
            # print(predecessor_map)
            # while start_state != predecessor_map[temp_node]: #moze problem z tym corner na koncu
            # print(predecessor_map[temp_node])
            # print(start_state,'start',predecessor_map[temp_node])
            # list_of_actions.append(predecessor_map[temp_node][1])
            # temp_node = predecessor_map[temp_node]
            # print(temp_node)

            # list_of_actions.reverse()
            # return list_of_actions
            return node[1]

        if not state in closed_set:
            closed_set.append(state)
            for succcessor in problem.getSuccessors(state):
                # predecessor_map[succcessor] = node
                new_actions = node[1] + [succcessor[1]]  # path until now + recent action
                frontier.push((succcessor[0], new_actions))


def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    start_state = problem.getStartState()
    frontier = util.PriorityQueue()  # access to the lowest priority item
    frontier.push(start_state, 0)  # the priority is the cost how to sum
    list_of_actions = []
    closed_set = []
    predecessor_map = {}
    cost_map = {}
    cost_map[start_state] = 0
    while frontier:
        node = frontier.pop()  # pop first in queue order by sum of costs

        if node == start_state:
            state = node

        else:
            state = node[0]

        if problem.isGoalState(state):
            temp_node = node
            # retrieval of solution
            list_of_actions.append(temp_node[1])
            while start_state != predecessor_map[temp_node]:
                list_of_actions.append(predecessor_map[temp_node][1])
                temp_node = predecessor_map[temp_node]
            list_of_actions.reverse()

            return list_of_actions

        if not state in closed_set:
            closed_set.append(state)

            for succcessor in problem.getSuccessors(state):

                if succcessor[0] not in closed_set:  # crucial otherwise infinite loop in one test case
                    cost_map[succcessor[0]] = cost_map[state] + succcessor[2]
                    predecessor_map[succcessor] = node
                    frontier.push(succcessor, cost_map[succcessor[0]])

    return []

    #util.raiseNotDefined()


def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # should be a bit faster less nodes expanded
    start_state = problem.getStartState()
    frontier = util.PriorityQueue()  # access to the lowest priority item
    frontier.push(start_state, 0)
    list_of_actions = []
    closed_set = []
    predecessor_map = {}
    cost_map = {}
    cost_map[start_state] = 0
    sum_h = 0
    while frontier:
        node = frontier.pop()  # pop first in queue order by sum of costs
        # print('expanded',node)

        if node == start_state:
            state = node

        else:
            state = node[0]

        if problem.isGoalState(state):
            temp_node = node
            # retrieval of solution
            list_of_actions.append(temp_node[1])
            while start_state != predecessor_map[temp_node]:
                list_of_actions.append(predecessor_map[temp_node][1])
                temp_node = predecessor_map[temp_node]
            list_of_actions.reverse()

            return list_of_actions

        # if not state in closed_set:
        #   closed_set.append(state)

        for succcessor in problem.getSuccessors(state):

            new_cost = cost_map[state] + succcessor[2]
            if succcessor[0] not in cost_map or new_cost < cost_map[succcessor[0]]:  # na start 0?
                # nie ekspanduje twice Some nodes may need to be expanded more than once to find the optimal path.
                cost_map[succcessor[0]] = cost_map[state] + succcessor[2]
                sum_h = cost_map[succcessor[0]] + heuristic(succcessor[0], problem)
                predecessor_map[succcessor] = node
                # print('juz loop',succcessor) # ten cheaper node whodzi tylko przy sorting?
                frontier.push(succcessor, sum_h)

    return []

    #util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
