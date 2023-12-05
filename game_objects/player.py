import time

import pygame
from pygame import Vector2

import config
from game_objects import Bullet
from game_objects.game_object import GameObject
from repositories import images


class Player(GameObject):
    def __init__(self, pos, vel, health: int, reload_seconds: int):
        super().__init__(images.get('player'), pos, vel)
        self.health = health
        self.reload_seconds = reload_seconds
        self.last_reload_time = time.process_time()
        self.reloading = False
        self.alive = True

    def tick(self, level):
        super().tick(level)
        delta = time.process_time() - self.last_reload_time
        self.reloading = delta <= self.reload_seconds

        if self.pos.x <= self.image.get_width() / 2:
            self.pos.x = self.image.get_width() / 2
        elif self.pos.x >= config.SCREEN_WIDTH - self.image.get_width() / 2:
            self.pos.x = config.SCREEN_WIDTH - self.image.get_width() / 2

    def start_reload(self):
        self.last_reload_time = time.process_time()

    def on_invader_bullet_collision(self, bullet, level):
        level.player.health -= 1
        if level.player.health <= 0:
            self.alive = False
        bullet.kill()

    def shoot(self, level):
        if level.player.reloading:
            return
        bullet = Bullet(pos=Vector2(0, 0),
                        vel=Vector2(0, -0.4),
                        shooter=self)
        level.bullets.add(bullet)
        self.start_reload()
        s = pygame.mixer.Sound("data/sounds/bullet.wav")
        s.set_volume(config.GAME_VOLUME)
        s.play()
