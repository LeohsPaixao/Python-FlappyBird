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
    ANIMATION_TIME = 5  # A cada 5 frames, a animação do passaro muda

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.height = self.y
        self.time = 0
        self.image_score = 0
        self.image = self.IMGS[0]

    def jump(self):
        self.speed = 10.5
        self.time = 0
        self.height = self.y

    def move_Bird(self):
        # Calcular o deslocamento
        self.time += 1
        displacement = 1.5 * (self.time**2) + self.speed * self.time

        # Restringir o deslocamento
        if displacement > 16:
            displacement = 16
        elif displacement < 0:
            displacement -= 2

        self.y += displacement

        # O Angulo do Passaro
        if displacement < 0 or self.y < (self.height + 50):
            if self.angle < self.ROTATION_MAX:
                self.angle = self.ROTATION_MAX
        else:
            if self.angle > -90:
                self.angle = self.ROTATION_SPEED

    def draw(self, screen):
        # Definir qual imagem do passaro usar
        self.image_score += 1

        if self.image_score < self.ANIMATION_TIME:
            self.image = self.IMGS[0]
        elif self.image_score < self.ANIMATION_TIME*2:
            self.image = self.IMGS[1]
        elif self.image_score < self.ANIMATION_TIME*3:
            self.image = self.IMGS[2]
        elif self.image_score < self.ANIMATION_TIME*4:
            self.image = self.IMGS[1]
        elif self.image_score < self.ANIMATION_TIME*4 + 1:
            self.image = self.IMGS[0]
            self.image_score = 0

        # Se o passaro tiver caindo, não bater as asas
        if self.angle <= 80:
            self.image = self.IMGS[1]
            self.image_score = self.ANIMATION_TIME*2

        # desenhar a imagem
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        pos_center_image = self.image.get_rect(topleft=(self.x, self.y)).center
        rectangle = rotated_image.get_rect(center=pos_center_image)
        screen.blit(rotated_image, rectangle.topleft)

    def get_mask(self):
        pygame.mask.from_surface(self.image)


class pipe:
    DISTANCE = 200  # 200 pixels
    SPEED = 5  # 5 pixels para esquerda

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.pos_top = 0
        self.pos_base = 0
        self.pos_top_image = pygame.transform.flip(PIPE_IMAGE, False, True)
        self.pos_base_image = PIPE_IMAGE
        self.passed = False
        self.set_height()


class floor:
    pass
