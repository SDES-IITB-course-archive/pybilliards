WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 140, 0)
FPS = 60
dispSize = dispWidth, dispHeight = 800, 500

scorecardSize = (800, 100)


no_of_balls = 1    # 3
my_ball_size = 30   # 25

import pygame
# import random
from math import *
pygame.init()

font = pygame.font.SysFont(None, 25)
gameDisplay = pygame.display.set_mode(dispSize)
# scoreDisplay = pygame.display.set_mode(scorecardSize)
pygame.display.set_caption('pyBilliard')
clock = pygame.time.Clock()
