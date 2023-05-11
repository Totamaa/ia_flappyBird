import random
import numpy as np
import pygame
import math
import sys

##### CONSTANTS #####

POPULATION = 100
WIDTH = 800
HEIGHT = 500
FPS = 45

generation = 0
bestScore = 0
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

class Population:
    def __init__(self, size):
        self.size = size
        self.birds = [Bird() for _ in range(size)]

    def update(self, pipes):
        for bird in self.birds:
            if bird.alive:
                bird.think(pipes)
                bird.score += 1
                bird.moove(pipes)

    def draw(self):
        for bird in self.birds:
            if bird.alive:
                bird.draw()
            
    def new_generation(self):
        new_birds = []
        
        for _ in range(self.size):
            parent = self.select_parent()
            child_brain = parent.brain.copy()
            child_brain.mutateSNN(0.25)
            child = Bird(child_brain)
            new_birds.append(child)
        
        self.birds = new_birds


    def select_parent(self):
        scores = [bird.score for bird in self.birds]
        return random.choices(self.birds, weights=scores)[0]

    def all_dead(self) -> bool:
        for bird in self.birds:
            if bird.alive:
                return False
        return True



class Bird:
    def __init__(self, brain=None):
        self.x = 100
        self.y = 300
        self.gravity = 0.5
        self.velocity = 0
        self.img = bird_img
        self.score = 0
        self.alive = True

        if brain is not None:
            self.brain = brain.copy()
        else:
            self.brain = SimpleNeuralNetwork(3, 6, 1)

    def jump(self):
        self.velocity = -10

    def moove(self, pipes):
        self.velocity += self.gravity
        self.y += self.velocity
        self.isAlive(pipes)

    def draw(self):
        if self.alive:
            screen.blit(self.img, (self.x, self.y))

    def think(self, pipes):
        closest_pipe = None
        closest_distance = float('inf')

        for pipe in pipes:
            distance = pipe.x + pipe_img.get_width() - self.x
            if distance > 0 and distance < closest_distance:
                closest_pipe = pipe
                closest_distance = distance

        inputs = np.zeros((3, 1))
        inputs[0, 0] = (self.y - closest_pipe.y) / HEIGHT
        inputs[1, 0] = (self.y - (closest_pipe.y - closest_pipe.space / 2)) / HEIGHT
        inputs[2, 0] = self.velocity / 10

        output = self.brain.forward(inputs)

        if output[0, 0] > 0.5:
            self.jump()
            
    def rect(self):
        return pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())

    def isAlive(self, pipes) -> bool:
        if not self.alive:  # If the bird is already dead, return False
            return False

        if self.y < 0 or self.y > HEIGHT:
            self.alive = False
            return False

        bird_rect = self.rect()
        for pipe in pipes:
            upper_pipe_rect, lower_pipe_rect = pipe.rects()
            if bird_rect.colliderect(upper_pipe_rect) or bird_rect.colliderect(lower_pipe_rect):
                self.alive = False
                return False

        return True


class Pipe:
    def __init__(self, x=WIDTH + pipe_img.get_width()) -> None:
        self.x = x
        midHeight = HEIGHT / 2
        self.y = random.randint(midHeight - 125, midHeight + 125)
        self.space = random.randint(150, 200)
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
    
    def rects(self):
        upper_rect = pygame.Rect(self.x, 0, self.img.get_width(), self.y - self.space / 2)
        lower_rect = pygame.Rect(self.x, self.y + self.space / 2, self.img.get_width(), HEIGHT - (self.y + self.space / 2))
        return upper_rect, lower_rect

    

class SimpleNeuralNetwork:
    def __init__(self, input_nodes, hidden_nodes, output_nodes):
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes
        self.weights_ih = np.random.randn(hidden_nodes, input_nodes)
        self.weights_ho = np.random.randn(output_nodes, hidden_nodes)
        self.bias_h = np.random.randn(hidden_nodes, 1)
        self.bias_o = np.random.randn(output_nodes, 1)

    def forward(self, inputs):
        hidden = np.dot(self.weights_ih, inputs)
        hidden += self.bias_h
        hidden = np.vectorize(sigmoid)(hidden)

        output = np.dot(self.weights_ho, hidden)
        output += self.bias_o
        output = np.vectorize(sigmoid)(output)

        return output
    
    def copy(self):
        new_nn = SimpleNeuralNetwork(self.input_nodes, self.hidden_nodes, self.output_nodes)
        new_nn.weights_ih = np.copy(self.weights_ih)
        new_nn.weights_ho = np.copy(self.weights_ho)
        new_nn.bias_h = np.copy(self.bias_h)
        new_nn.bias_o = np.copy(self.bias_o)
        return new_nn

    def mutateSNN(self, mutation_rate):
        self.weights_ih = mutate(self.weights_ih, mutation_rate)
        self.weights_ho = mutate(self.weights_ho, mutation_rate)
        self.bias_h = mutate(self.bias_h, mutation_rate)
        self.bias_o = mutate(self.bias_o, mutation_rate)

##### FUNCTIONS #####

def reset_game(pop):
    global pipeTable
    pipeTable = [Pipe()]
    
def draw_text(score, gen=generation, best=bestScore):
    textGeneration = font.render(f"Génération : {gen}", True, (255, 255, 255))
    screen.blit(textGeneration, (10, 10))
    
    if (score > 0):
        textScore = font.render(f"Score : {score}", True, (255, 255, 255))
        screen.blit(textScore, (10, 40))
    
    if (best > 0):
        textBestScore = font.render(f"Meilleur score : {best}", True, (255, 255, 255))
        screen.blit(textBestScore, (10, 70))
    
def check_passed_pipe(bird: Bird, pipe: Pipe) -> bool:
    if not pipe.passed and bird.x > pipe.x + pipe_img.get_width():
        pipe.passed = True
        return True
    return False

def mutate(weights, mutation_rate):
    new_weights = np.copy(weights)
    for i in range(new_weights.shape[0]):
        for j in range(new_weights.shape[1]):
            if np.random.rand() < mutation_rate:
                new_weights[i, j] += np.random.normal(0, 0.1)
    return new_weights


def sigmoid(x):
    x = np.clip(x, -500, 500)
    return 1 / (1 + math.exp(-x))


##### INSTANCES #####

population = Population(POPULATION)
population.draw()
pipeTable = [Pipe()]


##### GAME LOOP #####

while restart:
    reset_game(POPULATION)
    generation += 1
    running = True
    score = 0

    while running:
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                restart = False

        # Mettre à jour la position de l'oiseau et des tuyaux
        population.update(pipeTable)
        for pipe in pipeTable:
            pipe.moove()

        # Ajouter un nouveau tuyau si nécessaire
        if pipeTable[-1].x < WIDTH - (25 / 100 * WIDTH):
            pipeTable.append(Pipe())

        # Vérifier si tous les oiseaux sont morts
        if population.all_dead():
            running = False

        # Dessiner l'arrière-plan
        for i in range(3):
            screen.blit(background_img, (i * background_img.get_width(), 0))

        # Dessiner les tuyaux
        for pipe in pipeTable:
            if pipe.isOut():
                pipeTable.remove(pipe)
            pipe.draw()

        # Dessiner les oiseaux
        population.draw()

        # Dessiner la génération actuelle et le score
        draw_text(0, generation, 0)

        # Mettre à jour l'affichage
        pygame.display.flip()

        # Contrôler le nombre d'images par seconde
        clock.tick(FPS)

    # Nouvelle génération
    population.new_generation()
    pygame.time.delay(250)

pygame.quit()
sys.exit()