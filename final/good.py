#!python3
# -*- coding: utf-8 -*-
'''
公众号：Python代码大全
'''
from copy import copy, deepcopy
import pygame
from torch import Size
import game
from random import choice, randint
import random
import numpy as np
SCORE = 0
SOLID = 1
FRAGILE = 2
DEADLY = 3
BELT_LEFT = 4
BELT_RIGHT = 5
BODY = 6

GAME_ROW = 40
GAME_COL = 28
OBS_WIDTH = GAME_COL // 4
SIDE = 13
SCREEN_WIDTH = SIDE*GAME_COL  
SCREEN_HEIGHT = SIDE*GAME_ROW #520
COLOR = {SOLID: 0x00ffff, FRAGILE: 0xff5500, DEADLY: 0xff2222, SCORE: 0xcccccc,
        BELT_LEFT: 0xffff44, BELT_RIGHT: 0xff99ff, BODY: 0x00ff00}
CHOICE = [SOLID, SOLID, SOLID, FRAGILE, FRAGILE, BELT_LEFT, BELT_RIGHT, DEADLY]


class Barrier(object):
    def __init__(self, screen, opt=None):
        self.screen = screen
        if opt is None:
            self.type = choice(CHOICE)
        else:
            self.type = opt
        self.frag_touch = False
        self.frag_time = 12
        self.score = False
        self.belt_dire = 0
        self.belt_dire = pygame.K_LEFT if self.type == BELT_LEFT else pygame.K_RIGHT
        self.left = randint(0, SCREEN_WIDTH - 7 * SIDE - 1)
        top = SCREEN_HEIGHT - SIDE - 1
        self.rect = pygame.Rect(self.left, top, 7*SIDE, SIDE)

    def rise(self):
        if self.frag_touch:
            self.frag_time -= 1
        if self.frag_time == 0:
            return False
        self.rect.top -= 2
        return self.rect.top >= 0

    def draw_side(self, x, y):
        if self.type == SOLID:
            rect = pygame.Rect(x, y, SIDE, SIDE)
            self.screen.fill(COLOR[SOLID], rect)
        elif self.type == FRAGILE:
            rect = pygame.Rect(x+2, y, SIDE-4, SIDE)
            self.screen.fill(COLOR[FRAGILE], rect)
        elif self.type == BELT_LEFT or self.type == BELT_RIGHT:
            rect = pygame.Rect(x, y, SIDE, SIDE)
            pygame.draw.circle(self.screen, COLOR[self.type], rect.center, SIDE // 2 + 1)
        elif self.type == DEADLY:
            p1 = (x + SIDE//2 + 1, y)
            p2 = (x, y + SIDE)
            p3 = (x + SIDE, y + SIDE)
            points = [p1, p2, p3]
            pygame.draw.polygon(self.screen, COLOR[DEADLY], points)

    def draw(self):
        for i in range(7):
            self.draw_side(i*SIDE+self.rect.left, self.rect.top)


class Hell(game.Game):
    def __init__(self, title, size, fps=60):
        super(Hell, self).__init__(title, size, fps)
        self.last = 6 * SIDE
        self.dire = 0
        self.depth=5
        self.barrier = [Barrier(self.screen, SOLID)]
        self.body = pygame.Rect(self.barrier[0].rect.center[0], 200, SIDE, SIDE)
        self.bind_key([pygame.K_LEFT, pygame.K_RIGHT], self.move)
        self.bind_key_up([pygame.K_LEFT, pygame.K_RIGHT], self.unmove)
        self.bind_key(pygame.K_SPACE, self.pause)

    def deepCopy(self):
        state = Hell('copy',(SCREEN_WIDTH, SCREEN_HEIGHT))
        return state
        

    def move(self, key):
        self.dire = key

    def unmove(self, key):
        self.dire = 0

    def show_end(self):
        self.score-=100
        self.end = True

    def move_man(self, dire):
        if dire == 0:
            return True
        rect = self.body.copy()
        if dire == -1 or dire == pygame.K_LEFT:
            rect.left -= 1
        else:
            rect.left += 1
        if rect.left < 0 or rect.left + SIDE >= SCREEN_WIDTH:
            return False
        for ba in self.barrier:
            if rect.colliderect(ba.rect):
                return False
        self.body = rect
        return True


    def legalmove(self):
        temp=[]
        rect = self.body.copy()
        if(rect.left==0):
            temp=[0,1]
        elif(rect.left + SIDE+1 >= SCREEN_WIDTH):
            temp=[0,-1]
        else:          
            temp=[0,1,-1]
        return temp


    def get_score(self, ba):
        if self.body.top > ba.rect.top and not ba.score:
            self.score += 1
            ba.score = True

    def tget_score(self):
        for ba in self.barrier:
            if not self.body.colliderect(ba.rect):
                if self.body.top > ba.rect.top and not ba.score:
                    self.score += 1
                    ba.score = True
        if self.end:
            self.score =-100
        return self.score

    def to_hell(self):
        self.body.top += 2
        for ba in self.barrier:
            if not self.body.colliderect(ba.rect):
                self.get_score(ba)
                continue
            if ba.type == DEADLY:
                self.show_end()
                return
            self.body.top = ba.rect.top - SIDE - 2
            if ba.type == FRAGILE:
                ba.frag_touch = True
            elif ba.type == BELT_LEFT or ba.type == BELT_RIGHT:
                # self.body.left += ba.belt_dire
                self.move_man(ba.belt_dire)
            break

        top = self.body.top
        if top < 0 or top+SIDE >= SCREEN_HEIGHT:
            self.show_end()

    def create_barrier(self):
        solid = list(filter(lambda ba: ba.type == SOLID, self.barrier))
        if len(solid) < 1:
            self.barrier.append(Barrier(self.screen, SOLID))
        else:
            self.barrier.append(Barrier(self.screen))
        self.last = randint(3, 5) * SIDE


    def update(self):
        if self.end or self.is_pause:
            return
        self.last -= 1
        if self.last == 0:
            self.create_barrier()

        for ba in self.barrier:
            if not ba.rise():
                if ba.type == FRAGILE and ba.rect.top > 0:
                    self.score += 1
                self.barrier.remove(ba)
        self.move_man(self.dire)
        self.move_man(self.dire)
        
        self.to_hell()

    def draw(self, end=False):
        if self.end or self.is_pause:
            return
        self.screen.fill(0x000000)
        self.draw_score((0x3c,0x3c,0x3c))
    

        for ba in self.barrier:
            ba.draw()
        
        if not end:
            self.screen.fill(COLOR[BODY], self.body)
        else:
            self.screen.fill(COLOR[DEADLY], self.body)
        
        pygame.display.update()



hell = Hell("是男人就下一百层", (SCREEN_WIDTH, SCREEN_HEIGHT))
target_left=180
dir=0
current = hell.barrier[0] #current target barrier
danger = [] #list of deadly
lower = 520 #lower barrier
cur_pos = 0 #left or right
check = 0
good = 0

def get_distance_from_point_to_line(point, line_point1, line_point2):
   
    if line_point1 == line_point2:
        point_array = np.array(point )
        point1_array = np.array(line_point1)
        return np.linalg.norm(point_array -point1_array )
   
    A = line_point2[1] - line_point1[1]
    B = line_point1[0] - line_point2[0]
    C = (line_point1[1] - line_point2[1]) * line_point1[0] + \
        (line_point2[0] - line_point1[0]) * line_point1[1]
   
    distance = np.abs(A * point[0] + B * point[1] + C) / (np.sqrt(A**2 + B**2))
    return distance

while True: 
    for event in pygame.event.get():
        hell.handle_input(event)
    
    '''def Max_Value (gameState, d):
        if gameState.end or d == gameState.depth:
            return gameState.tget_score()
        temp=[]
        for action in gameState.legalmove() :
            gameState1=gameState
            gameState1.move_man(action)
            temp.append(Max_Value(gameState1, d+1))
        return max(temp)


    temp=[]
    for i in hell.legalmove():
        hell1=hell
        hell1.move_man(i)
        temp.append(Max_Value(hell1,0))
    
    maxscore=max(temp)
    bestIndices = [index for index in range(len(temp)) if temp[index] == maxscore]
    chosenIndex = random.choice(bestIndices)'''
    
    # print(current)
    # if(good == 0):
    #     ba = current
    #     if ba.type in [SOLID,BELT_LEFT, BELT_RIGHT] :
    #             if abs(180-ba.left)<abs(180-ba.left-91):
    #                 if ba.rect.top-hell.body.top>abs(hell.body.left-ba.rect.left):
                            
    #                         target_left=ba.left+1
    #                         dir=-1
    #             else:
    #                 if ba.rect.top-hell.body.top>abs(hell.body.left-ba.rect.left-91):
                            
    #                         target_left=ba.left+89
    #                         dir=1
    #     good = 1
    # else:

    for ba in reversed(hell.barrier): 
        danger = []
        check = 0
        if ba.type == DEADLY:
                danger.append([ba.rect.left-SIDE, ba.rect.top-SIDE, ba.rect.right+SIDE])

        if ba.type in [SOLID,BELT_LEFT, BELT_RIGHT] :
            if abs(180-ba.left)<abs(180-ba.left-91):
                if ba.rect.top-hell.body.top>abs(hell.body.left-ba.rect.left):
                        lower = ba.rect.top
                        cur_pos = 1
                        if(good == 1):
                            current = ba
                            good = 0
                        target_left=ba.left+1
                        dir=-1 #左
            else:
                if ba.rect.top-hell.body.top>abs(hell.body.left-ba.rect.left-91):
                        lower = ba.rect.top
                        good = 1
                        target_left=ba.left+89
                        dir=1
            
            for i in danger:
                point1 = [hell.body.left, hell.body.top+SIDE]
                point2 = [ba.rect.left, ba.rect.top]
                point3 = [hell.body.left+SIDE, hell.body.top+SIDE]
                point4 = [ba.rect.left+91, ba.rect.top]
                # if get_distance_from_point_to_line(i, point1, point2) == 0:
                #     check = 1
                #     break
                # if get_distance_from_point_to_line(i, point1, point2) == 0:
                #     check = 1
                #     break
                if dir == -1:
                    if(abs((point1[1] - point2[1]) / (point2[2] - point2[2])) > abs((point1[1] - i[1]) / (point2[2] - i[2]))):
                        check = 1
                        dir= -1
                        break
                    elif(abs((point3[1] - point4[1]) / (point3[2] - point4[2])) > abs((point3[1] - i[1]) / (point3[2] - i[2]))):
                        check = 1
                        dir = -1
                        dir=1
                        break
                    elif(abs((point1[1] - point2[1]) / (point2[2] - point2[2])) > abs((point1[1] - i[3]) / (point2[2] - i[2]))):
                        check = 1
                        break
                    elif(abs((point3[1] - point4[1]) / (point3[2] - point4[2])) > abs((point3[1] - i[3]) / (point3[2] - i[2]))):
                        check = 1
                        dir=1
                        break
            
            if check == 1:
                break
            
            
                
        
    if hell.body.top<100:  
        if dir==-1:
            hell.dire=-1
        else:
            hell.dire=1
    else:
        if hell.body.left<target_left:
            hell.dire=1
        elif hell.body.left==target_left:
            hell.dire=0
        else:
            hell.dire = -1 
    
    print (target_left)
    print(hell.body.top)
    hell.timer.tick(hell.fps)
    hell.update()
    hell.draw()






