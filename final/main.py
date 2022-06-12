import pygame
import game
from random import choice, randint
from numpy import random
SCORE = 0
SOLID = 1
FRAGILE = 2
DEADLY = 3
BELT_LEFT = 4
BELT_RIGHT = 5
BODY = 6

GAME_ROW = 40
GAME_COL = 28
OBS_WIDTH = GAME_COL // 4 #	取整除 - 返回商的整数部分（向下取整）
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
        self.frag_time = 30
        self.score = False
        self.belt_dire = 0
        self.belt_dire = pygame.K_LEFT if self.type == BELT_LEFT else pygame.K_RIGHT
        left = randint(0, SCREEN_WIDTH - 7 * SIDE - 1)
        top = SCREEN_HEIGHT - SIDE - 1
        self.rect = pygame.Rect(left, top, 7*SIDE, SIDE)

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
            rect = pygame.Rect(x, y, SIDE, SIDE)
            pygame.draw.polygon(self.screen, COLOR[DEADLY], points)

    def draw(self):
        for i in range(7):
            self.draw_side(i*SIDE+self.rect.left, self.rect.top)


class Hell(game.Game):
    def __init__(self, title, size, fps=60):
        super(Hell, self).__init__(title, size, fps)
        self.last = 6 * SIDE
        self.dire = 0
        self.barrier = [Barrier(self.screen, SOLID)]
        self.body = pygame.Rect(self.barrier[0].rect.center[0], 200, SIDE, SIDE)

        self.bind_key([pygame.K_LEFT, pygame.K_RIGHT], self.move)
        self.bind_key_up([pygame.K_LEFT, pygame.K_RIGHT], self.unmove)
        self.bind_key(pygame.K_SPACE, self.pause)

    def move(self, key):
        self.dire = key

    def unmove(self, key):
        self.dire = 0

    def show_end(self):
        self.draw(0, end=True)
        self.end = True

    def move_man(self, dire):
        if dire == 0:
            return True
        rect = self.body.copy()
        if dire == pygame.K_LEFT:
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

    def get_score(self, ba):
        if self.body.top > ba.rect.top and not ba.score:
            self.score += 1
            ba.score = True

    def to_hell(self):
        self.body.top += 2
        # print(len(self.barrier))
        for ba in self.barrier:
            if not self.body.colliderect(ba.rect):
                self.get_score(ba)
                continue
            if ba.type == DEADLY:
                # ba.frag_touch = False
                self.life = self.life-0.05;
                # print(self.life)
                
                if(self.life <= 0) :
                    self.show_end()
                # return
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
        self.last = randint(2, 4) * SIDE

    def update(self, current_time):
        print(self.body)
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
        # print(len(self.barrier))
        self.move_man(self.dire)
        self.move_man(self.dire)
        self.to_hell()

    def draw(self, current_time, end=False):
        if self.end or self.is_pause:
            return
        self.screen.fill(0x000000)
        self.draw_score((0x3c, 0x3c, 0x3c))
        life_rect = pygame.Rect(50, 50, SIDE, SIDE)
        self.draw_life((0xDC, 0x14, 0x3C), life_rect)
        for ba in self.barrier:
            ba.draw()
        if not end:
            self.screen.fill(COLOR[BODY], self.body)
        else:
            self.screen.fill(COLOR[DEADLY], self.body)
        pygame.display.update()

    def get_body(self):
        return self.body
    
    def get_barrier(self):
        return self.barrier

if __name__ == '__main__':
    hell = Hell("是男人就下一百层", (SCREEN_WIDTH, SCREEN_HEIGHT))
    hell.run()
while True: 
    for event in pygame.event.get():
        hell.handle_input(event)

    def Max_Value (gameState, d):
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
    chosenIndex = random.choice(bestIndices)

