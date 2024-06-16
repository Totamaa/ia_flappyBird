import pygame
from src.assets import bird_img
from src.constants import SCREEN_HEIGHT, BIRD_X, BIRD_Y, GRAVITY, JUMP_VELOCITY

class Bird(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.x: int = BIRD_X
        self.y: int = BIRD_Y
        self.gravity: float = GRAVITY
        self.velocity: float = 0
        self.image = bird_img
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.alive: bool = True

    def jump(self) -> None:
        """Make the bird jump"""
        self.velocity = JUMP_VELOCITY

    def move(self) -> None:
        """Update the bird's position"""
        self.velocity += self.gravity
        self.rect.y += self.velocity
        self.check_bounds()

    def check_bounds(self) -> None:
        """Check if the bird is out of the screen bounds"""
        if self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT:
            self.alive = False

    def update(self) -> None:
        """Update the bird's state"""
        if self.alive:
            self.move()

    def is_alive(self) -> bool:
        """Check if the bird is alive"""
        return self.alive
