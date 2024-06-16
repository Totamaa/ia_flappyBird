import pygame
import sys
from .constants import WIDTH, HEIGHT, FPS, FONT, PIPE_FREQUENCY, PLAYER_TYPE
from .assets import background_img
from .bird import Bird
from .pipe import Pipe
from .utils import draw_text

if PLAYER_TYPE == 'human':
    from .players.human import HumanPlayer

def init_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    return screen, clock

def reset_game():
    bird = Bird()
    pipes = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(bird)
    return bird, pipes, all_sprites

def handle_events(player, bird):
    player.handle_events(bird)

def update_game(bird, pipes, all_sprites):
    all_sprites.update()
    if pipes and pipes.sprites()[-1].rect.x < WIDTH - (PIPE_FREQUENCY * WIDTH):
        pipes.add(Pipe())
    for pipe in pipes:
        if pipe.check_collision(bird):
            return False
    return bird.is_alive()

def draw_game(screen, bird, pipes, all_sprites):
    screen.fill((0, 0, 0))
    for i in range(3):
        screen.blit(background_img, (i * background_img.get_width(), 0))
    all_sprites.draw(screen)
    draw_text(screen, FONT, "Score: 0", (10, 10))
    pygame.display.flip()

def main():
    screen, clock = init_game()
    bird, pipes, all_sprites = reset_game()
    running = True
    player = HumanPlayer() if PLAYER_TYPE == 'human' else None
    while running:
        handle_events(player, bird)
        running = update_game(bird, pipes, all_sprites)
        draw_game(screen, bird, pipes, all_sprites)
        clock.tick(FPS)
    pygame.quit()
    sys.exit()
