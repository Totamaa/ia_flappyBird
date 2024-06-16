import pygame

# Taille de la fenêtre
WIDTH = 800
HEIGHT = 500
FPS = 60

# Difficulté
PIPE_FREQUENCY = 0.25  # Plus c'est petit, plus il y a de tuyaux
CHANGEMENT_HAUTEUR_PIPE = 100  # Plus c'est grand, plus les tuyaux peuvent changer de hauteur
ECART_MIN = 125
ECART_MAX = 175

# Bird
BIRD_X = 100
BIRD_Y = 300
GRAVITY = 0.5
JUMP_VELOCITY = -10

# Joueur
PLAYER_TYPE = 'human'  # Peut être 'human' ou un autre type d'IA

# Pygame setup
pygame.font.init()
FONT = pygame.font.Font(None, 36)
