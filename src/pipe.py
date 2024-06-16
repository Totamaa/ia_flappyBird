import pygame
import random
from src.assets import pipe_img
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, PIPE_HEIGHT_CHANGE, GAP_MIN, GAP_MAX
from src.bird import Bird

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x: int = SCREEN_WIDTH + pipe_img.get_width()) -> None:
        super().__init__()
        self.image = pipe_img
        self.rect = self.image.get_rect()
        mid_height = SCREEN_HEIGHT // 2
        self.y = random.randint(mid_height - PIPE_HEIGHT_CHANGE, mid_height + PIPE_HEIGHT_CHANGE)
        self.gap = random.randint(GAP_MIN, GAP_MAX)
        self.rect.topleft = (x, self.y + self.gap // 2)
        self.passed: bool = False

    def update(self) -> None:
        """Move the pipe and remove it if it's out of the screen"""
        self.rect.x -= 5
        if self.rect.right < 0:
            self.kill()

    def check_collision(self, bird: Bird) -> bool:
        """Check if the pipe collides with the bird"""
        upper_rect = pygame.Rect(self.rect.x, 0, self.image.get_width(), self.y - self.gap // 2)
        lower_rect = pygame.Rect(self.rect.x, self.y + self.gap // 2, self.image.get_width(), SCREEN_HEIGHT - (self.y + self.gap // 2))
        if bird.rect.colliderect(upper_rect) or bird.rect.colliderect(lower_rect):
            bird.alive = False
            return True
        return False
