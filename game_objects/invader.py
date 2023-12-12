import random

import pygame
from pygame import Vector2

from settings import Settings
from game_objects import Player
from game_objects import Bullet
from game_objects import GameObject


class Invader(GameObject):
    def __init__(self, image, pos, vel, points: int, images):
        super().__init__(image, pos, vel)
        self.points = points
        self.images = images

    def tick(self, level):
        super().tick(level)

        if self.pos.x <= 50:
            self.pos += Vector2(0, 50)
            self.vel *= -1
        elif self.pos.x >= Settings.SCREEN_WIDTH - 50:
            self.pos += Vector2(0, 50)
            self.vel *= -1

        if level.player.pos.x + 20 >= self.pos.x >= level.player.pos.x - 20:
            if random.randint(1, 2000) == 1:
                self.shoot(level)

    def shoot(self, level):
        bullet = Bullet(pos=Vector2(0, 0), vel=Vector2(0, 0.4),
                        shooter=self, images=self.images)
        level.bullets.add(bullet)

    def on_bullet_collision(self, bullet):
        if isinstance(bullet.shooter, Player):
            bullet.shooter.points += self.points
            bullet.kill()
            self.kill()
