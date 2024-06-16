import pygame
from .assets import bird_img
from .constants import HEIGHT, BIRD_X, BIRD_Y, GRAVITY, JUMP_VELOCITY

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = BIRD_X
        self.y = BIRD_Y
        self.gravity = GRAVITY
        self.velocity = 0
        self.image = bird_img
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.alive = True

    def jump(self):
        self.velocity = JUMP_VELOCITY

    def move(self):
        self.velocity += self.gravity
        self.rect.y += self.velocity
        self.check_bounds()

    def check_bounds(self):
        if self.rect.y < 0 or self.rect.y > HEIGHT:
            self.alive = False

    def update(self):
        if self.alive:
            self.move()

    def is_alive(self):
        return self.alive
