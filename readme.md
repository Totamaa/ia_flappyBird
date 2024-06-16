# IA Flappy Bird

![Version](https://img.shields.io/badge/Version-v4.0.0-blueviolet)
![Langage](https://img.shields.io/badge/Langage-Python-0052cf)

## Sommaire

- [Sommaire](#sommaire)
- [Présentation du projet](#présentation-du-projet)
- [Installation](#installation)
- [Fonctionnalités](#fonctionnalités)
  - [Déjà existante](#déjà-existante)
    - [Jouer a Flappy Bird](#jouer-a-flappy-bird)
    - [Entrainer une IA pour jouer a flappy bird](#entrainer-une-ia-pour-jouer-a-flappy-bird)
  - [*À Venir*](#à-venir)
    - [Pour les humais](#pour-les-humais)
    - [Pour les IAs](#pour-les-ias)
- [Crédits](#crédits)

## Présentation du projet

Jeu Flappy bird, pour jouer ou pour entrainer une IA. Fait avec Pygame.

## Installation

1. Télécharger ou cloner le repos
   - v2.0.0: Flappy Bird pour Humains
   - v3.0.0: Flappy Bird pour IA
   - v4.0.0: Flappy Bird avec différent types d'IA
2. Télécharger Python
3. Lancer la commande `pip install -r requirements.txt`
4. Pour jouer ou faire jouer l'IA: `py game.py`

## Fonctionnalités

### Déjà existante

#### Jouer a Flappy Bird

Cliquer ou appuyer sur espace pour sauter, éviter les tuyaux et aller le plus loins possible.

#### Entrainer une IA pour jouer a flappy bird

Voir une IA s'entrainer sur flappy bird. C'est une IA qui utilise une représentation simplifiée de la séléction naturelle.
Il est possible de jouer sur certains paramètres, comme la population, le taux de mutations...
Il est également possible de jouer sur la difficulté du jeu, en ajustant le taux d'apparition des tuyaux, la différence de hauteurs etc...

### *À Venir*

#### Pour les humais

Une meilleure interface, avec le score, le meilleurs score, possibilité de choisir la difficulter etc...

#### Pour les IAs

Interface pour choisir les paramètres, changements de réseau de neuronnes avec différents paramètres en entrées. Choix du nombre de neuronnes sur la couche cachées, sur la couche d'entrée (dont choix des infos que percoit les oiseaux)

## Crédits

- Dev: **[Matteo Calderaro](https://github.com/Totamaa)** (premier projet pygame)
- Assets: **[Samuelcust](https://github.com/samuelcust/flappy-bird-assets)**
