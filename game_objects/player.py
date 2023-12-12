import time

from pygame import Vector2

from settings import Settings
from game_objects import Bullet
from game_objects.game_object import GameObject


class Player(GameObject):
    def __init__(self, pos, vel, health: int, reload_seconds: int,
                 images,
                 points: int = 0):
        super().__init__(images.get('player'), pos, vel)
        self.health = health
        self.reload_seconds = reload_seconds
        self.last_reload_time = time.process_time()
        self.reloading = False
        self.alive = True
        self.points = points
        self.images = images

    def tick(self, level):
        super().tick(level)
        delta = time.process_time() - self.last_reload_time
        self.reloading = delta <= self.reload_seconds

        if self.pos.x <= self.image.get_width() / 2:
            self.pos.x = self.image.get_width() / 2
        if self.pos.x >= Settings.SCREEN_WIDTH - self.image.get_width() / 2:
            self.pos.x = Settings.SCREEN_WIDTH - self.image.get_width() / 2

    def start_reload(self):
        self.last_reload_time = time.process_time()

    def on_invader_bullet_collision(self, bullet):
        self.health -= 1
        if self.health <= 0:
            self.alive = False
        bullet.kill()

    def on_invader_collision(self, invader):
        invader.kill()
        self.alive = False

    def shoot(self, level):
        if level.player.reloading:
            return
        bullet = Bullet(pos=Vector2(0, 0),
                        vel=Vector2(0, -0.4),
                        shooter=self,
                        images=self.images)
        level.bullets.add(bullet)
        self.start_reload()

    def move_left(self):
        self.vel = Vector2(-0.4, 0)

    def move_right(self):
        self.vel = Vector2(0.4, 0)
