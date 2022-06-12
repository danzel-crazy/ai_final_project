from main import Hell, agentState
import information
from  state import GameStateData
import pygame

class direction:
    def __init__(self):
    # ACTIONS = {pygame.K_LEFT: "left", pygame.K_RIGHT: "right", pygame.K_DOWN: "down"}
        self.left = pygame.K_LEFT
        self.right = pygame.K_RIGHT


class Actions:

    def getlegalKidActions(state):
        action = direction.left

        action = direction.right
        return action
    def appplyActions():
        return 0
# class agentstate:



class GameState:
    """
    A GameState specifies the full game state, including the food, capsules,
    agent configurations and score changes.

    GameStates are used by the Game object to capture the actual state of the game and
    can be used by agents to reason about the game.

    Much of the information in a GameState is stored in a GameStateData object.  We
    strongly suggest that you access that data via the accessor methods below rather
    than referring to the GameStateData object directly.

    Note that in classic Pacman, Pacman is always agent 0.
    """

    ####################################################
    # Accessor methods: use these to access state data #
    ####################################################

    # static variable keeps track of which states have had getLegalActions called
    explored = set()

    def getAndResetExplored():
        tmp = GameState.explored.copy()
        GameState.explored = set()
        return tmp
    getAndResetExplored = staticmethod(getAndResetExplored)
    def getLegalActions(self, agentIndex=0):
        """
        Returns the legal actions for the agent specified.
        """
#        GameState.explored.add(self)
        if Hell.is_end():
            return []
        else :
            return Actions.getlegalKidActions(self)

        # if agentIndex == 0:  # Pacman is moving
        #     return PacmanRules.getLegalActions(self)
        # else:
        #     return GhostRules.getLegalActions(self, agentIndex)

    def getNextState(self, agentIndex, action):
        """
        Returns the child state after the specified agent takes the action.
        """
        # Check that children exist
        if Hell.is_end():
            raise Exception('Can\'t generate a child of a terminal state.')
        
        # Copy current state
        state = GameState(self)

        Actions.appplyActions(state, action)

        # Let agent's logic deal with its action's effects on the board
        # if agentIndex == 0:  # Pacman is moving
        #     state.data._eaten = [False for i in range(state.getNumAgents())]
        #     PacmanRules.applyAction(state, action)
        # else:                # A ghost is moving
        #     GhostRules.applyAction(state, action, agentIndex)

        # Book keeping
        # state.data._agentMoved = agentIndex
        state.data.score += state.data.scoreChange
        GameState.explored.add(self)
        GameState.explored.add(state)
        return state

    def getLegalKidActions(self):
        return self.getLegalActions(0)

    def getKidNextState(self, action):
        """
        Generates the child state after the specified pacman move
        """
        return self.getNextState(0, action)

    def getKidState(self):
        """
        Returns an AgentState object for pacman (in game.py)

        state.pos gives the current position
        state.direction gives the travel vector
        """
        return self.data.agentStates[0].copy()

    def getKidPosition(self):
        return self.data.agentStates[0].getPosition()

    def getNumAgents(self):
        return len(self.data.agentStates)

    def getScore(self):
        return float(self.data.score)

    def getWalls(self):
        """
        Returns a Grid of boolean wall indicator variables.

        Grids can be accessed via list notation, so to check
        if there is a wall at (x,y), just call

        walls = state.getWalls()
        if walls[x][y] == True: ...
        """
        return self.data.layout.walls

    def hasFood(self, x, y):
        return self.data.food[x][y]

    def hasWall(self, x, y):
        return self.data.layout.walls[x][y]

    def isLose(self):
        return self.data._lose

    def isWin(self):
        return self.data._win

    #############################################
    #             Helper methods:               #
    # You shouldn't need to call these directly #
    #############################################

    def __init__(self, prevState=None):
        """
        Generates a new state by copying information from its predecessor.
        """
        if prevState != None:  # Initial state
            self.data = GameStateData(prevState.data)
        else:
            self.data = GameStateData()

    def deepCopy(self):
        state = GameState(self)
        state.data = self.data.deepCopy()
        return state

    def __eq__(self, other):
        """
        Allows two states to be compared.
        """
        return hasattr(other, 'data') and self.data == other.data

    def __hash__(self):
        """
        Allows states to be keys of dictionaries.
        """
        return hash(self.data)

    def __str__(self):

        return str(self.data)

    def initialize(self, inital_state):
        """
        Creates an initial game state from a layout array (see layout.py).
        """
        self.data.initialize(inital_state)