import pygame

# TOP = 24
# LEFT = 0
# WIDTH = 635
# HEIGHT = 455
# ORIGIN_WIDTH = 635
# ORIGIN_HEIGHT = 455
# ACTIONS = [
#     (Key.left,),
#     (Key.right,),
#     ()
# ]

# ORIGIN_LOSE_LOCATION = [225, 470]
# LOSE_LOCATION = [225, 470]
# LOSE_COLOR = [200, 208, 212,   0]

# PLAYER_COLOR = 160
# PIKE_COLOR = 96
# PLAYFORM_COLOR = 64
# N_PLATFORMS = 12

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

FOUR_NEIGH = {"left": (0, -1), "right": (0, 1), "up": (-1, 0), "down": (1, 0)}
EIGHT_NEIGH = list(FOUR_NEIGH.values()) + [(1, 1), (1, -1), (-1, 1), (-1, -1)]
STATES = {"left": (0, -1), "right": (0, 1), "down": (1, 0)}
ACTIONS = {pygame.K_LEFT: "left", pygame.K_RIGHT: "right", pygame.K_DOWN: "down"}

class direction:
    # ACTIONS = {pygame.K_LEFT: "left", pygame.K_RIGHT: "right", pygame.K_DOWN: "down"}
    left = pygame.K_LEFT
    right = pygame.K_RIGHT