import random
import sys

import pygame

import game_object


# Python class representing the whole game, control everything in a game.
class Game:
    def __init__(self, width, height, ground_y):
        pygame.init()
        pygame.display.set_caption("Block Jump")

        self.screen = pygame.display.set_mode((width, height))
        self.width = width
        self.height = height
        self.ground_y = ground_y
        self.clock = pygame.time.Clock()

        self.font1 = pygame.font.SysFont("Arial", 48)
        self.font2 = pygame.font.SysFont("Arial", 28)

        self.SPAWN_EVENT = pygame.USEREVENT + 1

        self.player = game_object.Block(ground_y=ground_y)

        self.player_group = pygame.sprite.GroupSingle()
        self.obstacles = pygame.sprite.Group()

        self.running = False
        self.playing = False
        self.initial = True
        self.collide = False

        self.player.rect.left = 6 * self.player.rect.width
        self.player_group.add(self.player)

        pygame.time.set_timer(self.SPAWN_EVENT, 1500)  # Spawn an obstacle every 1000 ms.

    def reset(self):
        self.playing = True
        self.collide = False

        self.player = game_object.Block(ground_y=self.ground_y)

        self.player_group = pygame.sprite.GroupSingle()
        self.obstacles = pygame.sprite.Group()

        self.player.rect.left = 6 * self.player.rect.width
        self.player_group.add(self.player)

    def run(self):
        self.running = True

        while self.running:
            self.clock.tick(60)

            if self.initial:
                self.draw()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.initial = False
                            self.playing = True

            if self.playing:
                # Handle events.
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        self.playing = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.player.jump()
                    elif event.type == self.SPAWN_EVENT:
                        obstacle = game_object.Obstacle(ground_y=self.ground_y)
                        obstacle.rect.left = self.width
                        self.obstacles.add(obstacle)

                # Update game.
                self.player_group.update()
                self.obstacles.update()

                if pygame.sprite.spritecollideany(sprite=self.player, group=self.obstacles):
                    self.playing = False
                    self.collide = True
                    self.draw()

                self.draw()

            else:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            self.reset()
                            self.playing = True
                    elif event.type == pygame.QUIT:
                        self.running = False

        pygame.quit()
        sys.exit()

    def draw(self):
        self.screen.fill((235, 235, 235))
        pygame.draw.rect(surface=self.screen, color=(0, 0, 0), rect=(0, self.ground_y, self.width, 3))

        self.player_group.draw(self.screen)
        self.obstacles.draw(self.screen)

        if self.initial:
            text1 = self.font1.render("Block Jump !", True, (0, 0, 0))
            text2 = self.font2.render("Press SPACE to start", True, (0, 0, 0))
            text1_rect = text1.get_rect(center=(self.width / 2, self.height * 0.1))
            text2_rect = text2.get_rect(center=(self.width / 2, self.height * 0.3))

            self.screen.blits(blit_sequence=[(text1, text1_rect), (text2, text2_rect)])

        if self.collide:
            text1 = self.font1.render("Game Over", True, (0, 0, 0))
            text2 = self.font2.render("Press R to start", True, (0, 0, 0))
            text1_rect = text1.get_rect(center=(self.width / 2, self.height * 0.1))
            text2_rect = text2.get_rect(center=(self.width / 2, self.height * 0.3))

            self.screen.blits(blit_sequence=[(text1, text1_rect), (text2, text2_rect)])

        pygame.display.flip()
