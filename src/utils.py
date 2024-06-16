import pygame
from typing import Tuple

def display_score(screen: pygame.Surface, font: pygame.font.Font, score: int, position: Tuple[int, int], color: Tuple[int, int, int] = (255, 255, 255)) -> None:
    """Display the score on the screen"""
    text = f"Score: {score}"
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, position)
