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
from pacman import GameState


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
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
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        score = 0
        distance_to_food = []
        distance_to_ghost = []

        if successorGameState.isWin():  # if is win then inf
            return float('inf')
        if newPos in newFood.asList():
            score = successorGameState.getScore() + 5  # if food than 5

        for i in newFood.asList():
            distance_to_food.append(manhattanDistance(newPos, i))
        score += 10 / min(distance_to_food)  # if small than better
        if len(distance_to_food) == 0:
            return float('inf')

        for i in successorGameState.getGhostPositions():
            distance_to_ghost.append(manhattanDistance(newPos, i))
        for i in distance_to_ghost:
            if i < 2:
                return (float("-inf"))  # too close
            elif i > 5:
                score += i  # score grows as the distance grows
        score -= 8 * len(newFood.asList())  # weight chosen experimentaly
        return score


def scoreEvaluationFunction(currentGameState: GameState):
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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        def minmax(state, depth, agentIndex):
            if self.depth == depth or state.isWin() or state.isLose():
                # reached the leaf
                return self.evaluationFunction(state)

            players = gameState.getNumAgents()  # fist one packman rest ghost
            if agentIndex == 0:
                maximum = float("-inf")
                for i in state.getLegalActions(agentIndex):
                    eval = minmax(state.generateSuccessor(agentIndex, i), depth, agentIndex + 1)
                    maximum = max(maximum, eval)  # choose max from the available options
                return maximum
            else:
                minimum = float("inf")
                nextAgent = (agentIndex + 1) % players
                nextDepth = depth
                if nextAgent == 0:
                    nextDepth += 1

                for i in state.getLegalActions(agentIndex):
                    eval = minmax(state.generateSuccessor(agentIndex, i), nextDepth, nextAgent)
                    minimum = min(minimum, eval)
                return minimum

        bestAction = None
        maximum = float("-inf")
        for action in gameState.getLegalActions(0):  # Pacman's turn
            evalValue = minmax(gameState.generateSuccessor(0, action), 0, 1)
            if evalValue > maximum:
                maximum = evalValue
                bestAction = action
        return bestAction


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        players = gameState.getNumAgents()

        def value(state, alpha, beta, agentIndex, depth):

            if depth == self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            # Max agent (Pacman)
            if agentIndex == 0:
                v = float('-inf')

                for action in state.getLegalActions(agentIndex):

                    v = max(v, value(state.generateSuccessor(agentIndex, action), alpha, beta, 1, depth))
                    alpha = max(alpha, v)
                    if v > beta:  # Beta cutoff
                        break
                return v

            # Min agent (Ghosts)
            else:
                v = float('inf')
                nextAgent = (agentIndex + 1) % players
                nextDepth = depth
                if nextAgent == 0:
                    nextDepth += 1

                for action in state.getLegalActions(agentIndex):
                    v = min(v, value(state.generateSuccessor(agentIndex, action), alpha, beta, nextAgent, nextDepth))
                    beta = min(beta, v)
                    if v < alpha:  # Alpha cutoff
                        break
                return v

        # Initialisation
        bestAction = None
        maximum = float("-inf")
        alpha = float('-inf')
        beta = float('inf')

        # Pacman's actions
        for action in gameState.getLegalActions(0):
            evalValue = value(gameState.generateSuccessor(0, action), alpha, beta, 1, 0)
            if evalValue > maximum:
                maximum = evalValue
                bestAction = action

            alpha = max(alpha, evalValue)

        return bestAction


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        players = gameState.getNumAgents();

        def value(state, depth, agentIndex):
            if depth == self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            if agentIndex == 0:
                v = float("-inf")
                for i in state.getLegalActions(agentIndex):
                    eval = value(state.generateSuccessor(agentIndex, i), depth, agentIndex + 1)
                    v = max(v, eval)  # choose max from the available options
                return v
            else:
                v = 0
                p = 1 / len(state.getLegalActions(agentIndex))
                nextAgent = (agentIndex + 1) % players
                nextDepth = depth
                if nextAgent == 0:
                    nextDepth += 1
                for i in state.getLegalActions(agentIndex):
                    eval = value(state.generateSuccessor(agentIndex, i), nextDepth, nextAgent)
                    v += p * eval
                return v

        bestAction = None
        maximum = float("-inf")
        for action in gameState.getLegalActions(0):  # Pacman's turn
            evalValue = value(gameState.generateSuccessor(0, action), 0, 1)
            if evalValue > maximum:
                maximum = evalValue
                bestAction = action
        return bestAction




def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # score=0
    # position=currentGameState.getPacmanPosition();
    # if currentGameState.isWin():
    #     score+=100
    # foods=currentGameState.getFood().asList()
    # for food in foods:
    #     if manhattanDistance(position,food)<2:
    #         score+=5
    #
    # capsules= currentGameState.getCapsules()
    # for capsule in capsules:
    #     if manhattanDistance(position,capsule)<5:
    #         score+=10
    # ghosts=currentGameState.getGhostPositions()
    # for ghost in ghosts:
    #     if manhattanDistance(position,ghost)<2:
    #         score-=10
    # #util.raiseNotDefined()
    # return score
    successorGameState = currentGameState
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    "*** YOUR CODE HERE ***"
    score = currentGameState.getScore()
    distance_to_food = []
    distance_to_ghost = []

    if successorGameState.isWin():  # if is win then inf
        return float('inf')
    if newPos in newFood.asList():
        score = successorGameState.getScore() + 5  # if food than 5

    for i in newFood.asList():
        distance_to_food.append(manhattanDistance(newPos, i))
    score += 10 / min(distance_to_food)  # jak male to fajnie
    if len(distance_to_food) == 0:
        return float('inf')

    for i in successorGameState.getGhostPositions():
        distance_to_ghost.append(manhattanDistance(newPos, i))
    for i in distance_to_ghost:
        if i < 2:
            return float("-inf")  # too close
        elif i > 5:
            score += i  # score grows as the distance grows
    for i in newScaredTimes:
        score += 5
    if newPos in successorGameState.getCapsules():
        score += 10

    score -= 8 * len(newFood.asList())  # weight chosen experimentaly
    return score


# Abbreviation
better = betterEvaluationFunction
