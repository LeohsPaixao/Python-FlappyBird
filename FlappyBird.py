import pygame
import os
import random
import neat


AI_PLAYING = True
generation = 0

SCREEN_WIDGHT = 500
SCREEN_HEIGHT = 800

PIPE_IMAGE = pygame.transform.scale2x(
    pygame.image.load(os.path.join('imgs', 'pipe.png')))
FLOOR_IMAGE = pygame.transform.scale2x(
    pygame.image.load(os.path.join('imgs', 'base.png')))
BACKGROUND_IMAGE = pygame.transform.scale2x(
    pygame.image.load(os.path.join('imgs', 'bg.png')))
BIRD_IMAGES = [
    pygame.transform.scale2x(pygame.image.load(
        os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(
        os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(
        os.path.join('imgs', 'bird3.png'))),
]

pygame.font.init()
FONT = pygame.font.SysFont('times new roman', 32)


class Bird:
    IMGS = BIRD_IMAGES
    # animações da rotação
    ROTATION_MAX = 25
    ROTATION_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.height = self.y
        self.time = 0
        self.score_image = 0
        self.image = self.IMGS[0]

    def jump(self):
        self.speed = -10.5
        self.time = 0
        self.height = self.y

    def move_bird(self):
        # calcular o deslocamento
        self.time += 1
        displacement = 1.5 * (self.time**2) + self.speed * self.time

        # restringir o deslocamento
        if displacement > 16:
            displacement = 16
        elif displacement < 0:
            displacement -= 2

        self.y += displacement

        # o angulo do passaro
        if displacement < 0 or self.y < (self.height + 50):
            if self.angle < self.ROTATION_MAX:
                self.angle = self.ROTATION_MAX
        else:
            if self.angle > -90:
                self.angle -= self.ROTATION_VEL

    def draw(self, screen):
        # definir qual imagem do passaro vai usar
        self.score_image += 1

        if self.score_image < self.ANIMATION_TIME:
            self.image = self.IMGS[0]
        elif self.score_image < self.ANIMATION_TIME*2:
            self.image = self.IMGS[1]
        elif self.score_image < self.ANIMATION_TIME*3:
            self.image = self.IMGS[2]
        elif self.score_image < self.ANIMATION_TIME*4:
            self.image = self.IMGS[1]
        elif self.score_image >= self.ANIMATION_TIME*4 + 1:
            self.image = self.IMGS[0]
            self.score_image = 0

        # se o passaro tiver caindo eu não vou bater asa
        if self.angle <= -80:
            self.image = self.IMGS[1]
            self.score_image = self.ANIMATION_TIME*2

        # desenhar a imagem
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        central_image_position = self.image.get_rect(
            topleft=(self.x, self.y)).center
        rectangle = rotated_image.get_rect(center=central_image_position)
        screen.blit(rotated_image, rectangle.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.image)


class Pipe:
    DISTANCE = 200
    PIPE_SPEED = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.pos_top = 0
        self.pos_base = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMAGE, False, True)
        self.PIPE_BASE = PIPE_IMAGE
        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.pos_top = self.height - self.PIPE_TOP.get_height()
        self.pos_base = self.height + self.DISTANCE

    def move_pipe(self):
        self.x -= self.PIPE_SPEED

    def draw(self, screen):
        screen.blit(self.PIPE_TOP, (self.x, self.pos_top))
        screen.blit(self.PIPE_BASE, (self.x, self.pos_base))

    def clash(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        base_mask = pygame.mask.from_surface(self.PIPE_BASE)

        distance_top = (self.x - bird.x, self.pos_top - round(bird.y))
        distance_base = (self.x - bird.x, self.pos_base - round(bird.y))

        top_point = bird_mask.overlap(top_mask, distance_top)
        base_point = bird_mask.overlap(base_mask, distance_base)

        if base_point or top_point:
            return True
        else:
            return False


class Floor:
    FLOOR_SPEED = 5
    WIDGHT = FLOOR_IMAGE.get_width()
    FLOORS_IMAGE = FLOOR_IMAGE

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDGHT

    def move_floor(self):
        self.x1 -= self.FLOOR_SPEED
        self.x2 -= self.FLOOR_SPEED

        if self.x1 + self.WIDGHT < 0:
            self.x1 = self.x2 + self.WIDGHT
        if self.x2 + self.WIDGHT < 0:
            self.x2 = self.x1 + self.WIDGHT

    def draw(self, screen):
        screen.blit(self.FLOORS_IMAGE, (self.x1, self.y))
        screen.blit(self.FLOORS_IMAGE, (self.x2, self.y))


def draw_screen(screen, birds, pipes, floor, points):
    screen.blit(BACKGROUND_IMAGE, (0, 0))
    for bird in birds:
        bird.draw(screen)
    for pipe in pipes:
        pipe.draw(screen)

    text = FONT.render(f"Pontuação: {points}", 1, (255, 255, 255))
    screen.blit(text, (SCREEN_WIDGHT - 10 - text.get_width(), 10))

    if AI_PLAYING:
        text = FONT.render(f"Geração: {generation}", 1, (255, 255, 255))
        screen.blit(text, (10, 10))

    floor.draw(screen)
    pygame.display.update()


def main(genomes, config):  # fitness function
    global generation
    generation += 1

    if AI_PLAYING:
        networks = []
        genome_list = []
        birds = []
        for _, genome in genomes:
            network = neat.nn.FeedForwardNetwork.create(genome, config)
            networks.append(network)
            genome.fitness = 0
            genome_list.append(genome)
            birds.append(Bird(230, 350))
    else:
        birds = [Bird(230, 350)]
    floor = Floor(730)
    pipes = [Pipe(700)]
    screen = pygame.display.set_mode((SCREEN_WIDGHT, SCREEN_HEIGHT))
    points = 0
    timer = pygame.time.Clock()

    starting = True
    while starting:
        timer.tick(60)  # Configura de 30 a 60 Frames.

        # interação com o usuário
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                starting = False
                pygame.quit()
                quit()
            if not AI_PLAYING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        for bird in birds:
                            bird.jump()

        pipe_index = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > (pipes[0].x + pipes[0].PIPE_TOP.get_width()):
                pipe_index = 1
        else:
            starting = False
            break

        # mover as coisas
        for i, bird in enumerate(birds):
            bird.move_bird()
            # aumentar um pouquinho a fitness do passaro
            genome_list[i].fitness += 0.1
            output = networks[i].activate((bird.y,
                                           abs(bird.y - pipes[pipe_index].height),
                                           abs(bird.y - pipes[pipe_index].pos_base)))
            # -1 e 1 -> se o output for > 0.5 então o passaro pula
            if output[0] > 0.5:
                bird.jump()
        floor.move_floor()

        add_pipe = False
        rm_pipes = []
        for pipe in pipes:
            for i, bird in enumerate(birds):
                if pipe.clash(bird):
                    birds.pop(i)
                    if AI_PLAYING:
                        genome_list[i].fitness -= 1
                        genome_list.pop(i)
                        networks.pop(i)
                if not pipe.passed and bird.x > pipe.x:
                    pipe.passed = True
                    add_pipe = True
            pipe.move_pipe()
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rm_pipes.append(pipe)

        if add_pipe:
            points += 1
            pipes.append(Pipe(600))
            for genome in genome_list:
                genome.fitness += 5
        for pipe in rm_pipes:
            pipes.remove(pipe)

        for i, bird in enumerate(birds):
            if (bird.y + bird.image.get_height()) > floor.y or bird.y < 0:
                birds.pop(i)
                if AI_PLAYING:
                    genome_list.pop(i)
                    networks.pop(i)

        draw_screen(screen, birds, pipes, floor, points)


def start(config_path):
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_path
                                )

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())

    if AI_PLAYING:
        population.run(main, 50)  # Roda em 50 gerações
    else:
        main(None, None)


if __name__ == '__main__':
    path = os.path.dirname(__file__)
    config_path = os.path.join(path, 'config.txt')
    start(config_path)
