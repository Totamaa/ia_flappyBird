import pygame
from typing import Tuple

def draw_text(screen: pygame.Surface, font: pygame.font.Font, text: str, position: Tuple[int, int], color: Tuple[int, int, int] = (255, 255, 255)) -> None:
    """Draw text on the screen"""
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, position)
