import pygame
from typing import NoReturn
from src.bird import Bird

class HumanPlayer:
    def handle_events(self, bird: Bird) -> NoReturn:
        """Handle events for human player"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.jump()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                bird.jump()
