import pygame
from pygame.sprite import Group

from game_objects.mystery_ship import MysteryShip
from game_objects.player import Player


class Level:
    def __init__(self, name: str,
                 invaders: Group,
                 bunkers: Group,
                 player: Player,
                 mystery_ship: MysteryShip):
        self.name = name
        self.invaders = invaders
        self.bunkers = bunkers
        self.player = player
        self.ship = mystery_ship
        self.bullets = pygame.sprite.Group()
        self.score_val: int = 0
        self.high_score: int = 0
