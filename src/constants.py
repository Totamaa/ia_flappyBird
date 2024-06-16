import pygame

# Screen size
SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 500
FPS: int = 60

# Difficulty settings
PIPE_FREQUENCY: float = 0.25  # Lower values mean more pipes
PIPE_HEIGHT_CHANGE: int = 100  # Higher values mean pipes can change height more
GAP_MIN: int = 125
GAP_MAX: int = 175

# Bird settings
BIRD_X: int = 100
BIRD_Y: int = 300
GRAVITY: float = 0.5
JUMP_VELOCITY: float = -10

# Player type
PLAYER_TYPE: str = 'human'  # Can be 'human' or another AI type

# Pygame setup
pygame.font.init()
FONT = pygame.font.Font(None, 36)