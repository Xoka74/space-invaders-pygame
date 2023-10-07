import random
from copy import copy
from dataclasses import dataclass, field

import pygame
from pygame import Surface, time
from pygame.math import Vector2
import time
import config
from repositories import images


@dataclass(unsafe_hash=True)
class GameObject(pygame.sprite.Sprite):
    sprite: Surface
    pos: Vector2
    vel: Vector2

    def __post_init__(self):
        super().__init__()

    @property
    def rect(self):
        return self.sprite.get_rect(center=self.pos)

    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos

    def get_distance(self, other):
        return self.pos.distance_to(other.pos) <= 50


@dataclass
class Invader(GameObject):
    points: int


@dataclass
class Bullet(GameObject):
    shooter: GameObject

    def __post_init__(self):
        self.pos = copy(self.shooter.pos)


@dataclass
class Player(GameObject):
    health: int
    reload_seconds: int
    last_reload_time: float = time.process_time()
    reloading: bool = False

    def __post_init__(self):
        self.last_reload_time = time.process_time() - self.reload_seconds

    def update(self):
        super().update()

        self.reloading = time.process_time() - self.last_reload_time <= self.reload_seconds

        if self.pos.x <= 0:
            self.pos.x = 0
        elif self.pos.x >= config.SCREEN_WIDTH:
            self.pos.x = config.SCREEN_WIDTH

    def reload(self):
        self.last_reload_time = time.process_time()


@dataclass
class Bunker(GameObject):
    state: int

    def update(self):
        self.sprite = images.get(f'bunker_{self.state}')


class OtherBunker(pygame.sprite.Sprite):
    def __init__(self, image: Surface, pos: Vector2, vel: Vector2):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.pos = pos
        self.vel = vel


@dataclass
class MysteryShip(GameObject):
    duration: float
    points: float
    started_time: float = time.process_time()
    started: bool = False

    def update(self):
        super().update()
        self.started = (time.process_time() - self.started_time) <= self.duration

        if self.pos.x <= 50:
            self.pos.x = 50
            self.vel *= -1
        elif self.pos.x >= config.SCREEN_WIDTH - 50:
            self.pos.x = config.SCREEN_WIDTH - 50
            self.vel *= -1


@dataclass
class Level:
    name: str
    invaders: list[Invader]
    bunkers: list[Bunker]
    player: Player
    bullets: list[Bullet] = field(default_factory=lambda: [])
    mystery_ship: MysteryShip = None
    score_val: int = 0

    def start_mystery_ship(self):
        random_y_cord = random.randint(0, config.SCREEN_WIDTH)
        self.mystery_ship = MysteryShip(images.get('mystery_ship'), Vector2(x=25, y=25), Vector2(1, 0),
                                        duration=5,
                                        points=100)

    def end_mystery_ship(self):
        self.mystery_ship = None
