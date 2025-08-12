import pygame


class Block(pygame.sprite.Sprite):
    def __init__(self, ground_y, gravity=1, jump_power=-17.5, width=30, height=60):
        super().__init__()

        self.image = pygame.Surface((width, height))  # Sprite.image must be assigned.
        self.rect = self.image.get_rect()  # Sprite.rect must be assigned.
        self.ground_y = ground_y
        self.v_speed = 0  # Initial velocity at vertical direction.
        self.gravity = gravity  # Gravity effect on velocity, direction down. The direction is opposite to v_speed.
        self.jump_power = jump_power  # Initial jump velocity, direction up.

        self.image.fill(color=(255, 0, 0))
        self.rect.bottom = ground_y  # The bottom of block is placed at y=260.

    def jump(self):
        if self.rect.bottom == self.ground_y:
            self.v_speed = self.jump_power

    # Sprite.update() must be override.
    def update(self):
        self.v_speed += self.gravity
        self.rect.bottom += self.v_speed  # Move block's y coordinate with velocity.

        # When the block lands, reset bottom coordinate and velocity.
        if self.rect.bottom >= self.ground_y:
            self.rect.bottom = self.ground_y
            self.v_speed = 0


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, ground_y, width=30, height=30):
        super().__init__()

        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()

        self.image.fill(color=(0, 0, 0))
        self.rect.bottom = ground_y

    def update(self):
        self.rect.left -= 5  # Obstacle moves to left 5 pixels per frame.

        if self.rect.right < 0:
            self.kill()
