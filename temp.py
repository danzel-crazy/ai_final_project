from HW.HW3.AI_HW3.util import manhattanDistance
import game
import main
import pyautogui
import cv2

# class Agent:
#     def __init__(self, action_space):
#         None
        
#     def getState(child):
#         distToCeil = child.y
#         distToBarrier = []
#         for barrier in self.getBarriers():
#             distToBarrier.append(manhattanDistance(child.getPosition(), barrier.getPosition()))

        
class ScreenData:
    def __init__(self):
        self.position = None
        self.distToceil = None
        self.distToBarrier = None
        self._lose = False
        self._win = False
    
    def getScreen(self):
        barrierNum = len(self.barrier)
        ''''''
    
    def getBarriers(self, idx):
        return self.barriers[idx]
    
    def getBarriersPositons(self):
        return [(barrier.body[1] , barrier.body[0]) for barrier in self.getBarriers]
        
    def getChildPosition(self):
        return (self.body[1], self.body[0])
        
class ai:    
    def evaluateFunction(self, action):
        pos = self.getPosition()
        seen = self.screen
    
    def computeDistance(self, curScreen):
        barriers = curScreen.getBarriers()
        curPos = curScreen.getChildPosition
        dist = []
        for ba in barriers:
            baPos = ba.getBarrierPosition()
            if baPos[1] > curPos[1] & ba.type != 3: 
                if abs(curPos[0] - baPos[0]) < abs(baPos[1] - curPos[1]) / 2:
                # check if reachable
                    dist.append(manhattanDistance(curPos, baPos))
        # type:
        # 1:blue 2:orange 3:red 4:yellow 5:purple
        for d in dist:
            print(dist)
        
        
        # move to that barrier 
            
        # total = 1000 * height + 100 * distToSafe - 100 * distToDead
        # return total
    