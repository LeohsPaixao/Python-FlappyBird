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


class Bird:
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
        # Animation Time(5 seg) * 2 = 10 seg
        elif self.image_score < self.ANIMATION_TIME*2:
            self.image = self.IMGS[1]
        # Animation Time(5 seg) * 3 = 15 seg
        elif self.image_score < self.ANIMATION_TIME*3:
            self.image = self.IMGS[2]
        # Animation Time(5 seg) * 4 =  20 seg
        elif self.image_score < self.ANIMATION_TIME*4:
            self.image = self.IMGS[1]
        # Animation Time((5 seg) * 4) + 1 = 21 seg
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


class Pipe:
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

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.pos_top = self.height - self.pos_top_image.get_height()
        self.pos_base = self.height + self.DISTANCE

    def move_Pipe(self):
        self.x -= self.SPEED

    def draw(self, screen):
        screen.blit(self.pos_base_image, (self.x, self.pos_top))
        screen.blit(self.pos_base_image, (self.x, self.pos_base))

    def clash(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.pos_top_image)
        base_mask = pygame.mask.from_surface(self.pos_base_image)

        distance_top = (self.x - bird.x, self.pos_top - round(bird.y))
        distance_base = (self.x - bird.x, self.pos_base - round(bird.y))

        clash_point_top = bird_mask.overlap(top_mask, distance_top)
        clash_point_base = bird_mask.overlap(base_mask, distance_base)

        if clash_point_base or clash_point_top:
            return True
        else:
            return False


class Floor:
    SPEED = 5
    WIDGHT = FLOOR_IMAGE.get_width()
    IMAGE = FLOOR_IMAGE

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDGHT

    def move(self):
        self.x1 -= self.SPEED
        self.x2 -= self.SPEED

        if self.x1 + self.WIDGHT < 0:
            self.x1 = self.x1 + self.WIDGHT
        if self.x2 + self.WIDGht < 0:
            self.x2 = self.x2 + self.WIDGHT

    def draw(self, screen):
        screen.blit(self.IMAGE, (self.x1, self.y))
        screen.blit(self.IMAGE, (self.x2, self.y))


def draw_screen(screen, birds, pipes, floor, point):
    screen.blit(BACKGROUND_IMAGE, (0, 0))
    for bird in birds:
        bird.draw(screen)
    for pipe in pipes:
        pipe.draw(screen)

    text = POINT_FONT.render(f"Pontuação: {point}", 1, (221, 217, 231))
    screen.blit(text, (SCREEN_WIDGHT - 10 - text.get_width(), 10))
    floor.draw(screen)
    pygame.display.update()


def main():
    birds = [Bird(230, 350)]
    floor = Floor(730)
    pipes = [Pipe(700)]
    screen = pygame.display.set_mode((SCREEN_WIDGHT, SCREEN_HEIGHT))
    point = 0
    timer = pygame.time.Clock()

    start = True
    while start:
        timer.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    for bird in birds:
                        bird.jump()

        for bird in birds:
            bird.move_Bird()
        floor.move()

        add_pipe = False
        rm_pipe = []
        for pipe in pipes:
            for i, bird in enumerate(birds):
                if pipe.clash(bird):
                    birds.pop(i)
                if not pipe.passed and bird.x > pipe.x:
                    pipe.passed = True
                    add_pipe = True
            pipe.move_Pipe()
            if pipe.x + pipe.pos_top_image() < 0:
                rm_pipe.append(pipe)

        if add_pipe:
            point += 1
            pipes.append(Pipe(600))
        for pipe in rm_pipe:
            pipes.remove(pipe)

        for i, bird in enumerate(birds):
            if (bird.y + bird.image.get_height()) > floor.y or bird.y < 0:
                birds.pop(i)

        draw_screen(screen, birds, pipes, floor, point)


if __name__ == '__main':
    main()
