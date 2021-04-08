import pygame
# import os
import random


SCREEN_WIDGHT = 500
SCREEN_HEIGHT = 800

PIPE_IMAGE = pygame.transform.scale2x(pygame.image.load('./imgs/pipe.png'))
FLOOR_IMAGE = pygame.transform.scale2x(pygame.image.load('./imgs/base.png'))
BACKGROUND_IMAGE = pygame.transform.scale2x(pygame.image.load('./imgs/bg.png'))
BIRD_IMAGES = [
    pygame.transform.scale2x(pygame.image.load('./imgs/bird1.png')),
    pygame.transform.scale2x(pygame.image.load('./imgs/bird2.png')),
    pygame.transform.scale2x(pygame.image.load('./imgs/bird3.png'))
]

pygame.font.init()
POINT_FONT = pygame.font.SysFont('Times New Roman', 32)


class bird:
    IMGS = BIRD_IMAGES
    ROTATION_MAX = 25
    ROTATION_SPEED = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.widght = self.y
        self.time = 0
        self.image_score = 0
        self.image = IMGS[0]

    


class pipe:
    pass


class floor:
    pass
