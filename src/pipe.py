import pygame
import random
from .assets import pipe_img
from .constants import WIDTH, HEIGHT, CHANGEMENT_HAUTEUR_PIPE, ECART_MIN, ECART_MAX

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x=WIDTH + pipe_img.get_width()):
        super().__init__()
        self.x = x
        mid_height = HEIGHT / 2
        self.y = random.randint(int(mid_height - CHANGEMENT_HAUTEUR_PIPE), int(mid_height + CHANGEMENT_HAUTEUR_PIPE))
        self.space = random.randint(ECART_MIN, ECART_MAX)
        self.image = pipe_img
        self.rect = self.image.get_rect(topleft=(self.x, self.y + self.space / 2))
        self.passed = False

    def move(self):
        self.rect.x -= 5

    def update(self):
        self.move()
        if self.rect.x < -self.image.get_width():
            self.kill()

    def check_collision(self, bird):
        upper_rect = pygame.Rect(self.rect.x, 0, self.image.get_width(), self.y - self.space / 2)
        lower_rect = pygame.Rect(self.rect.x, self.y + self.space / 2, self.image.get_width(), HEIGHT - (self.y + self.space / 2))
        if bird.rect.colliderect(upper_rect) or bird.rect.colliderect(lower_rect):
            bird.alive = False
            return True
        return False
