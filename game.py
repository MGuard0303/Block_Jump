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

        self.background_color = (235, 235, 235)
        self.font_color = (15, 15, 15)
        self.player_color = (235, 0, 0)
        self.obstacle_color = (15, 15, 15)

        self.background_color_dark = (30, 30, 30)
        self.font_color_dark = (245, 245, 245)
        self.player_color_dark = (245, 245, 245)
        self.obstacle_color_dark = (0, 191, 255)
        self.dark_mode = False

        self.font1 = pygame.font.SysFont("Chalkboard", 48)
        self.font2 = pygame.font.SysFont("Chalkboard", 24)

        self.SPAWN_EVENT = pygame.USEREVENT + 1
        self.CHANGE_RENDER_MODE = pygame.USEREVENT + 2

        self.player = game_object.Block(ground_y=ground_y)

        self.player_group = pygame.sprite.GroupSingle()
        self.obstacles = pygame.sprite.Group()

        self.running = False
        self.playing = False
        self.initial = True
        self.collide = False

        self.player.rect.left = 6 * self.player.rect.width
        self.player_group.add(self.player)

    def reset(self):
        self.playing = True
        self.collide = False

        self.player = game_object.Block(ground_y=self.ground_y)

        self.player_group = pygame.sprite.GroupSingle()
        self.obstacles = pygame.sprite.Group()

        if self.dark_mode:
            self.player.image.fill(self.player_color_dark)
        else:
            self.player.image.fill(self.player_color)

        self.player.rect.left = 6 * self.player.rect.width
        self.player_group.add(self.player)

    def run(self):
        millis = int(random.uniform(1, 3.5) * 1000)
        pygame.time.set_timer(self.SPAWN_EVENT, millis=millis)  # Spawn an obstacle every millis ms.
        pygame.time.set_timer(self.CHANGE_RENDER_MODE, millis=30 * 1000)

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
                        m1 = random.randint(1, 2)
                        m2 = random.randint(1, 2)
                        obstacle = game_object.Obstacle(ground_y=self.ground_y, width=30 * m1, height=30 * m2)

                        if self.dark_mode:
                            obstacle.image.fill(self.obstacle_color_dark)
                        else:
                            obstacle.image.fill(self.obstacle_color)

                        obstacle.rect.left = self.width
                        self.obstacles.add(obstacle)

                    elif event.type == self.CHANGE_RENDER_MODE:
                        self.dark_mode = not self.dark_mode

                        for ele in self.obstacles:
                            if self.dark_mode:
                                ele.image.fill(self.obstacle_color_dark)
                            else:
                                ele.image.fill(self.obstacle_color)

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
        if self.dark_mode:
            self.screen.fill(self.background_color_dark)
            self.player.image.fill(self.player_color_dark)
            pygame.draw.rect(surface=self.screen, color=self.font_color_dark, rect=(0, self.ground_y, self.width, 3))
        else:
            self.screen.fill(self.background_color)
            self.player.image.fill(self.player_color)
            pygame.draw.rect(surface=self.screen, color=self.font_color, rect=(0, self.ground_y, self.width, 3))

        self.player_group.draw(self.screen)
        self.obstacles.draw(self.screen)

        if self.initial:
            if self.dark_mode:
                text1 = self.font1.render("Block Jump !", True, self.font_color_dark)
                text2 = self.font2.render("Press SPACE to start", True, self.font_color_dark)
                text1_rect = text1.get_rect(center=(self.width / 2, self.height * 0.1))
                text2_rect = text2.get_rect(center=(self.width / 2, self.height * 0.3))
            else:
                text1 = self.font1.render("Block Jump !", True, self.font_color)
                text2 = self.font2.render("Press SPACE to start", True, self.font_color)
                text1_rect = text1.get_rect(center=(self.width / 2, self.height * 0.1))
                text2_rect = text2.get_rect(center=(self.width / 2, self.height * 0.3))

            self.screen.blits(blit_sequence=[(text1, text1_rect), (text2, text2_rect)])

        if self.collide:
            if self.dark_mode:
                text1 = self.font1.render("Game Over", True, self.font_color_dark)
                text2 = self.font2.render("Press R to start", True, self.font_color_dark)
                text1_rect = text1.get_rect(center=(self.width / 2, self.height * 0.1))
                text2_rect = text2.get_rect(center=(self.width / 2, self.height * 0.3))
            else:
                text1 = self.font1.render("Game Over", True, self.font_color)
                text2 = self.font2.render("Press R to start", True, self.font_color)
                text1_rect = text1.get_rect(center=(self.width / 2, self.height * 0.1))
                text2_rect = text2.get_rect(center=(self.width / 2, self.height * 0.3))

            self.screen.blits(blit_sequence=[(text1, text1_rect), (text2, text2_rect)])

        pygame.display.flip()
