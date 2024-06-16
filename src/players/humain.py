import pygame

class HumanPlayer:
    def handle_events(self, bird):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.jump()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # clic gauche
                bird.jump()
