#!python3
# -*- coding: utf-8 -*-
'''
公众号：Python代码大全
'''
import copy 
import pygame
import game
from random import choice, randint
import random
import numpy as np


average = 0
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
SCREEN_HEIGHT = SIDE*GAME_ROW
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
        self.kid_pos = [self.body.left, self.body.top, self.body[2], self.body[3]]
        self.barrier_pos = None
        self.new_kid_pos = [self.body.left, self.body.top, self.body[2], self.body[3]]
        self.new_barrier_pos = None

    def create(self):
        # print(self.barrier)
        self.kid_pos = self.new_kid_pos
        temp  = []
        for ba in self.barrier:
                temp.append([ba.type, ba.rect.left, ba.rect.top, 91])
                # print(temp)
        self.barrier_pos = temp
    
    def new_create(self):
        # print(self.barrier)
        self.new_kid_pos = [self.body.left, self.body.top, self.body[2], self.body[3]]
        temp  = []
        for ba in self.barrier:
            temp.append([ba.type, ba.rect.left, ba.rect.top, 91])
        self.new_barrier_pos =  temp

    def deepCopy(self):
        state = Hell('copy',(SCREEN_WIDTH, SCREEN_HEIGHT))
        return state
        

    def move(self, key):
        self.dire = key

    def unmove(self, key):
        self.dire = 0

    def show_end(self):
        self.end = True
        self.draw()
        global average 
        average += self.score
            
        # print(self.score)

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
        # state = deepcopy(self)
        # print(rect)  
        if(self.body.left==0):
            temp=[0,1]
        elif(self.body.left + SIDE+1 >= SCREEN_WIDTH):
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


    def update(self,action):
        # print(self.barrier_pos)
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
        self.create()
        
        self.move_man(action)
        self.move_man(action)

        self.to_hell()
        self.new_create()

    def draw(self):
        if self.end or self.is_pause:
            return
        self.screen.fill(0x000000)
        self.draw_score((0x3c,0x3c,0x3c))
    

        for ba in self.barrier:
            ba.draw()
        
        if not self.end:
            self.screen.fill(COLOR[BODY], self.body)
        else:
            self.screen.fill(COLOR[DEADLY], self.body)
        
        pygame.display.update()


class gameState:
    def __init__(self):
        self.end = 0
        self.depth = 5
        self.kid_pos = None
        self.barrier_pos = None
        self.new_kid_pos = None
        self.new_barrier_pos = None
        self.score = 0
        self.action = 0

    def legalmove(self):
        temp=[]
        # print(rect)  
        # self.end = game.show_end()
        if(self.new_kid_pos == None) :
            return [0,1,-1]
        else:
            if(self.new_kid_pos[0]==0):
                temp=[0,1]
            elif(self.new_kid_pos[0] + SIDE+1 >= SCREEN_WIDTH):
                temp=[0,-1]
            else:          
                temp=[0,1,-1]
            
            # print(temp)
            return temp
    def move_man(self, action):
        self.action = action
        self.new_kid_pos[0] += action
        
        return self

    def tget_score(self):
        reward = 0
        distance = 0
        
        if self.new_barrier_pos != None:
            index = len(self.new_barrier_pos)
            for ba in reversed(self.new_barrier_pos): 
                if ba[0] == SOLID :
                    distance = manhattan_distance([ba[1], ba[2]], [self.new_kid_pos[0], self.new_kid_pos[1]])
                    if(ba[2] >= 270):
                        reward -= abs(ba[1] - self.new_kid_pos[0]) 
                    else:
                        reward -= abs(ba[1] - self.new_kid_pos[0]) 
                    
                if ba[0] == BELT_LEFT :
                    if(ba[2] >= 270):
                        reward -= abs(ba[1]+91 - self.new_kid_pos[0]-SIDE) 
                    else:
                        reward -= abs(ba[1]+91 - self.new_kid_pos[0]-SIDE)
                if ba[0] == BELT_RIGHT :
                    if(ba[2] >= 270):
                        reward -= abs(ba[1] - self.new_kid_pos[0])
                    else:
                        reward -= abs(ba[1] - self.new_kid_pos[0])
                    
                if ba[0] == DEADLY :
                    distance = manhattan_distance([ba[1]- (13*3), ba[2]+(13*3)], [self.new_kid_pos[0], self.new_kid_pos[1]])
                    if ba[1] <= self.new_kid_pos[0] <= ba[1]+91:
                        reward += abs(ba[1] - self.new_kid_pos[0])
                    else:
                        reward += abs(ba[1]-SIDE - self.new_kid_pos[0]) 
                reward *= index
                index -=1
                
        # print(self.action)
        # print(reward)
        return reward       

    def update(self):
        self.kid_pos = self.new_kid_pos
        if self.new_barrier_pos != None:
            for ba in self.new_barrier_pos:
                if self.new_kid_pos[1]+SIDE-2 <= ba[2] and ba[1] <= self.new_kid_pos[0] <= ba[1]+91:
                    self.new_kid_pos = self.new_kid_pos
                else:
                    self.new_kid_pos = [self.new_kid_pos[0], self.new_kid_pos[1]+2, self.new_kid_pos[2], self.new_kid_pos[3]]
            # 
        else:
            self.new_kid_pos = [self.new_kid_pos[0], self.new_kid_pos[1]+2, self.new_kid_pos[2], self.new_kid_pos[3]]
        
        top = self.new_kid_pos[1]
        if top < 0 or top+SIDE >= SCREEN_HEIGHT:
            self.end = True
        # left, to top,... 
    def new_create(self):
        # print(self.barrier)
        if self.new_barrier_pos != None :
            self.barrier_pos = self.new_barrier_pos
            temp  = []
            for ba in self.new_barrier_pos:
                if(ba[2]-2 > SIDE):
                    temp.append([ba[0], ba[1], ba[2]-2, 91])
            self.new_barrier_pos =  temp

    def getnextState(self, current):
        self.kid_pos = current[0]
        self.barrier_pos = current[1]
        self.new_kid_pos = current[2]
        self.new_barrier_pos = current[3]
        self.end = current[4]
        self.action = current[5]
        # print(self.kid_state)

def manhattan_distance(point1, point2):
        distance = 0
        for x1, x2 in zip(point1, point2):
            difference = x2 - x1
            
            absolute_difference = abs(difference)
            distance += absolute_difference

        # print(distance)
        return distance

index = 10
time = index
while(index):
    # print(index)
    index -=1
    hell = Hell("是男人就下一百层", (SCREEN_WIDTH, SCREEN_HEIGHT))
    # print(hell.end)
    target_left=182
    dir=0
    current = 0;
    
    i = 10
    while hell.end!=True: 
        for event in pygame.event.get():
            hell.handle_input(event)
        current = [hell.kid_pos, hell.barrier_pos, hell.new_kid_pos, hell.new_barrier_pos, hell.end, 0]
        # print(current)
        # print(current[0])
        # print(current[2])
        def Max_Value (game, d):
            best_action = None
            best_score = None
            # print(type(game))
            if game.end or d == game.depth:
                return None, game.tget_score()
            temp = []
            for action in game.legalmove() :
                # print(action)
                gameState1 = copy.deepcopy(game) 
                gameState1.move_man(action)
                state = [gameState1.kid_pos, gameState1.barrier_pos, gameState1.new_kid_pos, gameState1.new_barrier_pos, gameState1.end, action]
                
                next_state = gameState()
                next_state.getnextState(state)
                
                next_state.new_create()
                next_state.update()
                # print([next_state.kid_pos, next_state.barrier_pos, next_state.new_kid_pos, next_state.new_barrier_pos, next_state.end, next_state.action])
                cur_action, cur_score = Max_Value(next_state, d+1)
                # print([action, cur_score])
                temp.append([action, cur_score])
            
            maxscore = None
            for i in temp:
                if maxscore == None or i[1] > maxscore :
                    maxscore = i[1]
            bestIndices = [index for index in temp if index[1] == maxscore]
            # print(bestIndices)
            best_action , best_score = random.choice(bestIndices)
            return best_action , best_score 


        temp=[]
        # for i in hell.legalmove():
        #     hell1= deepcopy(hell)
        #     hell1.move_man(i)
        #     temp.append(Max_Value(hell1,0))
        g = gameState()
        g.getnextState(current)
        # print(type(g))
        temp = Max_Value(g, 0)
        # print(temp)
        # hell.move_man(temp[0])
        # hell.move_man(temp[0])
        
        hell.timer.tick(hell.fps)
        hell.update(temp[0])
        hell.draw()
        
print("average:", average/time)
   






