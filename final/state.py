from msilib.schema import Class
from main import Hell
import game

class GameStateData():
    def __init__(self, prevState=None):
        """
        Generates a new data packet by copying information from its predecessor.
        """
        if prevState != None:
            self.food = prevState.food.shallowCopy()
            self.capsules = prevState.capsules[:]
            self.agentStates = self.copyAgentStates(prevState.agentStates)
            self.layout = prevState.layout
            self._eaten = prevState._eaten
            self.score = prevState.score

        self._littlekid = None
        self._barrier = None
        self._deadly = None
        self._solid = None
        self._fragile = None
        self._lose = False
        self.scoreChange = 0
    
    def get_value (self ):
        self._littlekid = Hell.get_body()
        self._barrier = Hell.get_barrier()
        self._deadly = None
        self._solid = None
        self._fragile = None
        self._lose = False
        self.scoreChange = 0
        
class agentstate():
    def __init__(self):
        self.start = 1
        self.position = Hell.get_body()
        self.barrier = Hell.get_barrier()
        self.score = game.Game.score
        self.life = 10;
        self.direction = 0;
        
    def copy(self):
        state = agentstate()
        state.position = self.position
        state.barrier = self.barrier
        state.score = self.score
        state.life = self.life
        state.direction = self.direction
        return state

    def getPosition(self):
        return self.position

    def getDirection(self):
        return self.direction

    def check(self):
        print(self.position)
        print(self.barrier)
        print(self.score)
        print(self.life)
        print(self.direction)
