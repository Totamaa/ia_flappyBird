import random
import numpy as np
import pygame

##### CONSTANTS #####

WIDTH = 800
HEIGHT = 500
FPS = 45

generation = 0
pygame.font.init()
font = pygame.font.Font(None, 36)

##### PYGAME SETUP #####
random.seed()
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
restart = True

##### LOAD IMAGES #####

background_img = pygame.image.load("./assets/background.png")
bird_img = pygame.image.load("./assets/bird.png")
pipe_img = pygame.image.load("./assets/pipe.png")

##### OBJECTS #####

class Bird:
    def __init__(self):
        self.x = 100
        self.y = 300
        self.gravity = 0.5
        self.velocity = 0
        self.img = bird_img

    def jump(self):
        self.velocity = -10

    def moove(self):
        self.velocity += self.gravity
        self.y += self.velocity

    def draw(self):
        screen.blit(self.img, (self.x, self.y))

    def isAlive(self, pipes) -> bool:
        if bird.y < 0 or bird.y > HEIGHT:
            return False

        for pipe in pipes:
            if pipe.x < bird.x + bird_img.get_width() and pipe.x + pipe_img.get_width() > bird.x:
                if bird.y < pipe.y - pipe.space / 2 or bird.y > pipe.y + pipe.space / 2:
                    return False

        return True

class Pipe:
    def __init__(self, x=WIDTH + pipe_img.get_width()) -> None:
        self.x = x
        midHeight = HEIGHT / 2
        self.y = random.randint(midHeight - 100, midHeight + 100)
        self.space = random.randint(175, 200)
        self.img = pipe_img
        self.passed = False

    def moove(self):
        self.x -= 5

    def draw(self):
        screen.blit(self.img, (self.x, self.y + self.space / 2))
        screen.blit(pygame.transform.flip(self.img, False, True), (self.x, (self.y - self.space / 2) - self.img.get_height()))

    def isOut(self) -> bool:
        if self.x < -pipe_img.get_width() * 6:
            return True
        return False

##### FUNCTIONS #####

def reset_game():
    global bird, pipeTable
    bird = Bird()
    pipeTable = [Pipe()]
    
def draw_generation(gen):
    text = font.render(f"Génération : {gen}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

##### INSTANCES #####

bird = Bird()
bird.draw()
pipeTable = [Pipe()]


##### GAME LOOP #####

while restart:
    reset_game()
    generation += 1
    running = True

    while running:
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                restart = False


        # Mettre à jour la position de l'oiseau et des tuyaux
        bird.moove()
        for pipe in pipeTable:
            pipe.moove()

        # Ajouter un nouveau tuyau si nécessaire
        if pipeTable[-1].x < WIDTH - (25 / 100 * WIDTH):
            pipeTable.append(Pipe())

        # Vérifier si l'oiseau est encore en vie
        if not bird.isAlive(pipes=pipeTable):
            running = False

        # Dessiner l'arrière-plan
        for i in range(3):
            screen.blit(background_img, (i * background_img.get_width(), 0))

        # Dessiner les tuyaux
        for pipe in pipeTable:
            if pipe.isOut():
                pipeTable.remove(pipe)
            pipe.draw()

        # Dessiner l'oiseau
        bird.draw()

        # Dessiner la génération actuelle
        draw_generation(generation)

        # Mettre à jour l'affichage
        pygame.display.flip()

        # Contrôler le nombre d'images par seconde
        clock.tick(FPS)
        
    pygame.time.delay(250)