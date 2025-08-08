import pygame


class Block(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.shape = pygame.Surface((20, 40))
        self.shape.fill(color=(0, 0, 0))
        self.rect = self.shape.get_rect()
        self.rect.bottom = 260  # The bottom of block is placed at y=260.
        self.velocity = 0,  # Velocity at vertical direction.
        self.gravity = 1,  # Gravity effect on velocity, direction down.
        self.jump_power = -15  # Initial jump velocity, direction up.

    def jump(self):
        if self.rect.bottom == 260:
            self.velocity = self.jump_power

    def update(self):
        self.velocity += self.gravity
        self.rect.y += self.velocity  # Move block's y coordinate with velocity.

        # When the block lands, reset bottom coordinate and velocity.
        if self.rect.bottom >= 260:
            self.rect.bottom = 260
            self.velocity = 0


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.shape = pygame.Surface((20, 20))
        self.shape.fill(color=(0, 255, 0))
        self.rect = self.shape.get_rect()
        self.rect.x = 800
        self.rect.bottom = 260

    def update(self):
        self.rect.x -= 5  # Obstacle moves to left 5 pixels per frame.

        if self.rect.right < 0:
            self.kill()
