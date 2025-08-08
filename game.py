import random

import pygame

import game_object


# Python class representing the whole game, control everything in a game.
class Game:
    def __init__(
            self,
            width=800,
            height=300,
            ground_y=260,  # Ground y coordinate.
            fps=60,
            spawn_interval_frames=(60, 120),  # Obstacle spawns interval.
    ):
        pygame.init()

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Block Jump")
        self.clock = pygame.time.Clock()
        self.fps = fps

        # Game screen parameters.
        self.width = width
        self.height = height
        self.ground_y = ground_y

        # Parameters to control how soon to spawn the next obstacle.
        self.spawn_min, self.spawn_max = spawn_interval_frames
        self.spawn_timer = 0
        self.next_spawn = random.randint(self.spawn_min, self.spawn_max)

        self.all_sprites = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()

        self.block = game_object.Block()
        self.block.rect.bottom = self.ground_y
        self.all_sprites.add(self.block)

        self.running = True

    def event_process(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    self.block.jump()

    # TODO
