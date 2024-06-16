import pygame

def draw_text(screen, font, text, position, color=(255, 255, 255)):
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, position)
