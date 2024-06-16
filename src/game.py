import pygame
import sys
from typing import Tuple
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, FONT, PIPE_FREQUENCY, PLAYER_TYPE
from src.assets import background_img
from src.bird import Bird
from src.pipe import Pipe
from src.utils import display_score

if PLAYER_TYPE == 'human':
    from src.players.human import HumanPlayer

def init_game() -> Tuple[pygame.Surface, pygame.time.Clock]:
    """Initialize the game"""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    return screen, clock

def reset_game() -> Tuple[Bird, pygame.sprite.Group, pygame.sprite.Group, int]:
    """Reset the game to the initial state"""
    bird = Bird()
    pipes = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(bird)
    score = 0
    return bird, pipes, all_sprites, score

def handle_events(player: HumanPlayer, bird: Bird) -> None:
    """Handle events for the player"""
    player.handle_events(bird)

def update_game(bird: Bird, pipes: pygame.sprite.Group, all_sprites: pygame.sprite.Group, score: int) -> Tuple[bool, int]:
    """Update the game state and return the updated score"""
    all_sprites.update()
    if not pipes or pipes.sprites()[-1].rect.x < SCREEN_WIDTH - (PIPE_FREQUENCY * SCREEN_WIDTH):
        pipe = Pipe()
        pipes.add(pipe)
        all_sprites.add(pipe)
    for pipe in pipes:
        if pipe.check_collision(bird):
            return False, score
        if not pipe.passed and pipe.rect.right < bird.rect.left:
            pipe.passed = True
            score += 1
    return bird.is_alive(), score

def draw_game(screen: pygame.Surface, all_sprites: pygame.sprite.Group, pipes: pygame.sprite.Group, score: int) -> None:
    """Draw all game elements on the screen"""
    screen.fill((0, 0, 0))
    for i in range(3):
        screen.blit(background_img, (i * background_img.get_width(), 0))
    for sprite in all_sprites:
        if isinstance(sprite, Pipe):
            sprite.draw(screen)
        else:
            screen.blit(sprite.image, sprite.rect)
    display_score(screen, FONT, score, (10, 10))
    pygame.display.flip()

def main() -> None:
    """Main game loop"""
    screen, clock = init_game()
    bird, pipes, all_sprites, score = reset_game()
    running = True
    player = HumanPlayer() if PLAYER_TYPE == 'human' else None
    while running:
        handle_events(player, bird)
        running, score = update_game(bird, pipes, all_sprites, score)
        draw_game(screen, all_sprites, pipes, score)
        clock.tick(FPS)
    pygame.quit()
    sys.exit()
