import random

import pygame
from pygame import Vector2

import config
from game_objects import Player
from game_objects import Bullet
from game_objects import GameObject


class Invader(GameObject):
    def __init__(self, image, pos, vel, points: int):
        super().__init__(image, pos, vel)
        self.points = points

    def tick(self, level):
        super().tick(level)

        if self.pos.x <= 50:
            self.pos += Vector2(0, 50)
            self.vel *= -1
        elif self.pos.x >= config.SCREEN_WIDTH - 50:
            self.pos += Vector2(0, 50)
            self.vel *= -1

        if level.player.pos.x + 20 >= self.pos.x >= level.player.pos.x - 20:
            if random.randint(1, 2000) == 1:
                bullet = Bullet(pos=Vector2(0, 0), vel=Vector2(0, 0.4),
                                shooter=self)
                level.bullets.add(bullet)

    def on_bullet_collision(self, bullet, level):
        if isinstance(bullet.shooter, Player):
            level.score_val += self.points
            bullet.kill()
            self.kill()
            s = pygame.mixer.Sound("data/sounds/explosion.wav")
            s.set_volume(config.GAME_VOLUME * 2)
            s.play()
