import random
import time

from pygame import Vector2
import config
from game_objects.game_object import GameObject
from repositories import images


class MysteryShip(GameObject):
    def __init__(self, pos, vel, duration, points):
        super().__init__(images.get('mystery_ship'), pos, vel)
        self.duration = duration
        self.points = points
        self.started_time = time.process_time()
        self.started = False

    def tick(self, level):
        super().tick(level)
        if (time.process_time() - self.started_time) >= self.duration:
            self.end()

        if not self.started:
            return

        if self.pos.x <= 50:
            self.pos.x = 50
            self.vel *= -1
        elif self.pos.x >= config.SCREEN_WIDTH - 50:
            self.pos.x = config.SCREEN_WIDTH - 50
            self.vel *= -1

    def on_bullet_collision(self, bullet, level):
        if level.ship.started:
            level.score_val += level.ship.points
            level.ship.end()
            bullet.kill()

    def start(self):
        self.pos = Vector2(x=random.randint(0, config.SCREEN_WIDTH),
                           y=25)
        self.started = True
        self.started_time = time.process_time()

    def end(self):
        self.started = False
        self.kill()
