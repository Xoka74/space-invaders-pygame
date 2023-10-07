import random
from copy import copy

import pygame
from pygame import Surface, time
from pygame.math import Vector2
import time

from pygame.sprite import Group

import config
from repositories import images


class GameObject(pygame.sprite.Sprite):
    def __init__(self, image: Surface, pos: Vector2, vel: Vector2):
        super().__init__()
        self.image = image
        self.pos = pos
        self.vel = vel
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos


class Invader(GameObject):
    def __init__(self, image, pos, vel, points: int):
        super().__init__(image, pos, vel)
        self.points = points


class Bullet(GameObject):
    def __init__(self, pos, vel, shooter: GameObject):
        super().__init__(images.get('bullet'), pos, vel)
        self.shooter = shooter
        self.pos = copy(self.shooter.pos)


class Player(GameObject):
    def __init__(self, pos, vel, health: int, reload_seconds: int):
        super().__init__(images.get('player'), pos, vel)
        self.health = health
        self.reload_seconds = reload_seconds
        self.last_reload_time = time.process_time()
        self.reloading = False

    def update(self):
        super().update()

        self.reloading = time.process_time() - self.last_reload_time <= self.reload_seconds

        if self.pos.x <= self.image.get_width() / 2:
            self.pos.x = self.image.get_width() / 2
        elif self.pos.x >= config.SCREEN_WIDTH - self.image.get_width() / 2:
            self.pos.x = config.SCREEN_WIDTH - self.image.get_width() / 2

    def reload(self):
        self.last_reload_time = time.process_time()


class Bunker(GameObject):
    def __init__(self, pos, vel, state: int):
        super().__init__(images.get('bunker_default'), pos, vel)
        self.state = state

    def update(self):
        self.image = images.get(f'bunker_{self.state}')


class MysteryShip(GameObject):
    def __init__(self, pos, vel, duration, points):
        super().__init__(images.get('mystery_ship'), pos, vel)
        self.duration = duration
        self.points = points
        self.started_time = time.process_time()
        self.started = False

    def update(self):
        super().update()
        if (time.process_time() - self.started_time) >= self.duration:
            self.end()

        if self.pos.x <= 50:
            self.pos.x = 50
            self.vel *= -1
        elif self.pos.x >= config.SCREEN_WIDTH - 50:
            self.pos.x = config.SCREEN_WIDTH - 50
            self.vel *= -1

    def start(self):
        self.pos = Vector2(x=random.randint(0, config.SCREEN_WIDTH), y=25)
        self.started = True
        self.started_time = time.process_time()

    def end(self):
        self.started = False
        self.kill()


class Level:
    def __init__(self, name: str, invaders: Group, bunkers: Group, player: Player, mystery_ship: MysteryShip):
        self.name = name
        self.invaders = invaders
        self.bunkers = bunkers
        self.player = player
        self.mystery_ship = mystery_ship
        self.bullets = pygame.sprite.Group()
        self.score_val: int = 0
        self.high_score: int = 0
