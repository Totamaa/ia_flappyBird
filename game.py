import random
import numpy as np
import pygame
import math
import sys

##### CONSTANTS #####

# taille de la fenêtre
WIDTH = 800
HEIGHT = 500
FPS = 45

# difficulté
PIPE_FREQUENCY = 25 / 100 # plus c'est petit, plus il y a de tuyaux
CHANGEMENT_HAUTEUR_PIPE = 100 # plus c'est grand, plus les tuyaux peuvent changer de hauteur
ECART_MIN = 125 # ecarts minimum entre les tuyaux (plus c'est petit, plus c'est dur)
ECART_MAX = 200 # ecarts maximum entre les tuyaux (plus c'est grand, plus c'est facile)

# ia
POPULATION = 150 # nombre d'oiseaux par génération
TAUX_DE_MUTATION = 0.1 # chance de mutation de chaque enfant oiseau par rapport à son parent


##### VARIABLES #####

generation = 0
bestScore = 0


##### PYGAME SETUP #####

pygame.font.init()
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
random.seed()
running = True
restart = True


##### LOAD IMAGES #####

background_img = pygame.image.load("./assets/background.png")
bird_img = pygame.image.load("./assets/bird.png")
pipe_img = pygame.image.load("./assets/pipe.png")
font = pygame.font.Font(None, 36)


##### OBJECTS #####

class Population:
    """ Classe qui gère la population d'oiseaux
    """
    def __init__(self, size):
        """initialise la population d'oiseaux

        Args:
            size (number): taille de la population
        """
        self.size = size
        self.birds = [Bird() for _ in range(size)]

    def update(self, pipes) -> None:
        """Met a jour la position, le score le cerveau et l'etat de chaque oiseau

        Args:
            pipes (Pipe[]): tableau contenant les tuyaux
        """
        for bird in self.birds:
            if bird.alive:
                bird.think(pipes)
                bird.score += 1
                bird.moove(pipes)

    def draw(self) -> None:
        """Desine chaque oiseau
        """
        for bird in self.birds:
            if bird.alive:
                bird.draw()
            
    def new_generation(self) -> None:
        """Crée une nouvelle génération d'oiseaux a partir des meilleurs de la génération précédente
        """
        new_birds = []
        
        for _ in range(self.size):
            parent = self.select_parent()
            child_brain = parent.brain.copy()
            child_brain.mutateSNN(TAUX_DE_MUTATION)
            child = Bird(child_brain)
            new_birds.append(child)
        
        self.birds = new_birds


    def select_parent(self):
        """selectionne un oiseau en fonction de son score pour etre un parent, plus l'oiseau a un score élevé, plus il a de chance d'etre selectionné

        Returns:
            Bird: parent selectionné
        """
        scores = [bird.score for bird in self.birds]
        poids = [(score - min(scores)) / (max(scores) - min(scores) + 1e-8) for score in scores]
        
        if sum(poids) == 0:
            return random.choice(self.birds)
        return random.choices(self.birds, weights=poids)[0]

    def all_dead(self) -> bool:
        """Verifie si tous les oiseaux sont morts

        Returns:
            bool: True si tous les oiseaux sont morts, False sinon
        """
        for bird in self.birds:
            if bird.alive:
                return False
        return True



class Bird:
    """Oiseau qui doit passer entre les tuyaux
    """
    def __init__(self, brain=None):
        """Crée un oiseau

        Args:
            brain (SimpleNeuralNetwork, optional): réseau de neurones de l'oiseau. Defaults to None.
        """
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
        """Fait sauter l'oiseau
        """
        self.velocity = -10

    def moove(self, pipes):
        """Met a jour la position de l'oiseau ainsi que son état

        Args:
            pipes (Pipe[]): tableau contenant les tuyaux
        """
        self.velocity += self.gravity
        self.y += self.velocity
        self.isAlive(pipes)

    def draw(self):
        """dessine l'oiseau
        """
        if self.alive:
            screen.blit(self.img, (self.x, self.y))

    def think(self, pipes):
        """Fait penser l'oiseau, c'est a dire qu'il va prendre une décision en fonction de son environnement

        Args:
            pipes (Pipe[]): tableau contenant les tuyaux
        """
        closest_pipe = None
        closest_distance = float('inf')

        for pipe in pipes:
            distance = pipe.x + pipe_img.get_width() - self.x
            if distance > 0 and distance < closest_distance:
                closest_pipe = pipe
                closest_distance = distance

        inputs = np.zeros((3, 1))
        inputs[0, 0] = (self.y - closest_pipe.y) / HEIGHT # Normalisation de la distance entre l'oiseau et le tuyau
        inputs[1, 0] = (self.y - (closest_pipe.y - closest_pipe.space / 2)) / HEIGHT # Normalisation de la distance entre l'oiseau et le haut du tuyau
        inputs[2, 0] = self.velocity / 10 # Normalisation de la vitesse de l'oiseau

        output = self.brain.forward(inputs)

        if output[0, 0] > 0.5:
            self.jump()
            
    def rect(self):
        """Retourne le rectangle de l'oiseau

        Returns:
            pygame.Rect: rectangle de l'oiseau
        """
        return pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())

    def isAlive(self, pipes) -> bool:
        """Verifie si l'oiseau est toujours en vie

        Args:
            pipes (Pipe[]): tableau contenant les tuyaux

        Returns:
            bool: True si l'oiseau est en vie, False sinon
        """
        if not self.alive:
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
    """Tuyau que l'oiseau doit passer, il y a un tuyau en haut et un en bas dans une instance de cette classe
    """
    def __init__(self) -> None:
        """Crée une paire de tuyaux
        """
        self.x = WIDTH + pipe_img.get_width()
        midHeight = HEIGHT / 2
        self.y = random.randint(midHeight - CHANGEMENT_HAUTEUR_PIPE, midHeight + CHANGEMENT_HAUTEUR_PIPE)
        self.space = random.randint(ECART_MIN, ECART_MAX)
        self.img = pipe_img
        self.passed = False

    def moove(self):
        """Met a jour la position des tuyaux
        """
        self.x -= 5

    def draw(self):
        """Dessine les tuyaux
        """
        screen.blit(self.img, (self.x, self.y + self.space / 2))
        screen.blit(pygame.transform.flip(self.img, False, True), (self.x, (self.y - self.space / 2) - self.img.get_height()))

    def isOut(self) -> bool:
        """Verifie si les tuyaux sont sortis de l'écran
        Il y a une marge de 6 tuyaux pour éviter des bugs d'affichage

        Returns:
            bool: True si les tuyaux sont sortis de l'écran, False sinon
        """
        if self.x < -pipe_img.get_width() * 6:
            return True
        return False
    
    def rects(self):
        """Retourne les rectangles des tuyaux

        Returns:
            (pygame.Rect, pygame.Rect): rectangle du tuyau du haut et du bas
        """
        upper_rect = pygame.Rect(self.x, 0, self.img.get_width(), self.y - self.space / 2)
        lower_rect = pygame.Rect(self.x, self.y + self.space / 2, self.img.get_width(), HEIGHT - (self.y + self.space / 2))
        return upper_rect, lower_rect

    

class SimpleNeuralNetwork:
    """Réseau de neurones simple représentant le cerveau de l'oiseau
    """
    def __init__(self, input_nodes, hidden_nodes, output_nodes):
        """Initialise le réseau de neurones

        Args:
            input_nodes (number): nombre de neurones en entrée
            hidden_nodes (number): nombre de neurones cachés
            output_nodes (number): nombre de neurones en sortie
        """
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes
        # initialisation des poids et des biais
        self.weights_ih = np.random.randn(hidden_nodes, input_nodes) 
        self.weights_ho = np.random.randn(output_nodes, hidden_nodes)
        self.bias_h = np.random.randn(hidden_nodes, 1)
        self.bias_o = np.random.randn(output_nodes, 1)

    def forward(self, inputs):
        """Calcule la sortie du réseau de neurones donc l'action de l'oiseau

        Args:
            inputs : Première couche du réseau de neurones

        Returns:
            number: choix de l'oiseau, 0 pour ne pas sauter, 1 pour sauter
        """
        hidden = np.dot(self.weights_ih, inputs)
        hidden += self.bias_h
        hidden = np.vectorize(sigmoid)(hidden)

        output = np.dot(self.weights_ho, hidden)
        output += self.bias_o
        output = np.vectorize(sigmoid)(output)

        return output
    
    def copy(self):
        """Copie le réseau de neurones

        Returns:
            SimpleNeuralNetwork: copie du réseau de neurones
        """
        new_nn = SimpleNeuralNetwork(self.input_nodes, self.hidden_nodes, self.output_nodes)
        new_nn.weights_ih = np.copy(self.weights_ih)
        new_nn.weights_ho = np.copy(self.weights_ho)
        new_nn.bias_h = np.copy(self.bias_h)
        new_nn.bias_o = np.copy(self.bias_o)
        return new_nn

    def mutateSNN(self, mutation_rate):
        """Modifie le réseau de neurones en fonction du taux de mutation, permet d'avoir des enfants oiseaux légèrement différents du parent

        Args:
            mutation_rate (number): taux de mutation (chance qu'un poids ou un biais soit modifié)
        """
        self.weights_ih = mutate(self.weights_ih, mutation_rate)
        self.weights_ho = mutate(self.weights_ho, mutation_rate)
        self.bias_h = mutate(self.bias_h, mutation_rate)
        self.bias_o = mutate(self.bias_o, mutation_rate)

##### FUNCTIONS #####

def reset_game():
    """Réinitialise le jeu
    """
    global pipeTable
    pipeTable = [Pipe()]
    
def draw_text(score, gen=generation, best=bestScore):
    """Dessine le texte en haut à gauche de l'écran

    Args:
        score (number): score de l'oiseau
        gen (number, optional): numéro de la génération. Defaults to generation.
        best (number, optional): meilleur score atteint. Defaults to bestScore.
    """
    textGeneration = font.render(f"Génération : {gen}", True, (255, 255, 255))
    screen.blit(textGeneration, (10, 10))
    
    if (score > 0):
        textScore = font.render(f"Score : {score}", True, (255, 255, 255))
        screen.blit(textScore, (10, 40))
    
    if (best > 0):
        textBestScore = font.render(f"Meilleur score : {best}", True, (255, 255, 255))
        screen.blit(textBestScore, (10, 70))
    
def check_passed_pipe(bird: Bird, pipe: Pipe) -> bool:
    """Vérifie si l'oiseau a passé le tuyau 

    Args:
        bird (Bird): oiseau a vérifier
        pipe (Pipe): tuyau a vérifier

    Returns:
        bool: True si l'oiseau a passé le tuyau, False sinon
    """
    if not pipe.passed and bird.x > pipe.x + pipe_img.get_width():
        pipe.passed = True
        return True
    return False

def mutate(weights, mutation_rate):
    """Modifie les poids en fonction du taux de mutation

    Args:
        weights (number): poid à modifier
        mutation_rate (number): taux de mutation (chance qu'un poids soit modifié)

    Returns:
        number: poids modifié
    """
    new_weights = np.copy(weights)
    for i in range(new_weights.shape[0]):
        for j in range(new_weights.shape[1]):
            if np.random.rand() < mutation_rate:
                new_weights[i, j] += np.random.normal(0, 0.1)
    return new_weights


def sigmoid(x):
    """Fonction d'activation sigmoid

    Args:
        x (number): valeur à passer dans la fonction

    Returns:
        number: valeur après passage dans la fonction sigmoid
    """
    x = np.clip(x, -1000, 1000)
    return 1 / (1 + math.exp(-x))


##### INSTANCES #####

population = Population(POPULATION)
population.draw()
pipeTable = [Pipe()]


##### GAME LOOP #####

while restart:
    reset_game()
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
        if pipeTable[-1].x < WIDTH - (PIPE_FREQUENCY * WIDTH):
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