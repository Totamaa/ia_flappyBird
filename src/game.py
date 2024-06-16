import pygame
import sys
from typing import Tuple
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, FONT, PIPE_FREQUENCY, PLAYER_TYPE
from src.assets import background_img
from src.bird import Bird
from src.pipe import Pipe
from src.utils import draw_text

if PLAYER_TYPE == 'human':
    from src.players.human import HumanPlayer

def init_game() -> Tuple[pygame.Surface, pygame.time.Clock]:
    """Initialize the game"""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    return screen, clock

def reset_game() -> Tuple[Bird, pygame.sprite.Group, pygame.sprite.Group]:
    """Reset the game to the initial state"""
    bird = Bird()
    pipes = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(bird)
    return bird, pipes, all_sprites

def handle_events(player: HumanPlayer, bird: Bird) -> None:
    """Handle events for the player"""
    player.handle_events(bird)

def update_game(bird: Bird, pipes: pygame.sprite.Group, all_sprites: pygame.sprite.Group) -> bool:
    """Update the game state"""
    all_sprites.update()
    if not pipes or pipes.sprites()[-1].rect.x < SCREEN_WIDTH - (PIPE_FREQUENCY * SCREEN_WIDTH):
        pipe = Pipe()
        pipes.add(pipe)
        all_sprites.add(pipe)
    for pipe in pipes:
        if pipe.check_collision(bird):
            return False
    return bird.is_alive()

def draw_game(screen: pygame.Surface, all_sprites: pygame.sprite.Group) -> None:
    """Draw all game elements on the screen"""
    screen.fill((0, 0, 0))
    for i in range(3):
        screen.blit(background_img, (i * background_img.get_width(), 0))
    all_sprites.draw(screen)
    draw_text(screen, FONT, "Score: 0", (10, 10))
    pygame.display.flip()

def main() -> None:
    """Main game loop"""
    screen, clock = init_game()
    bird, pipes, all_sprites = reset_game()
    running = True
    player = HumanPlayer() if PLAYER_TYPE == 'human' else None
    while running:
        handle_events(player, bird)
        running = update_game(bird, pipes, all_sprites)
        draw_game(screen, all_sprites)
        clock.tick(FPS)
    pygame.quit()
    sys.exit()
