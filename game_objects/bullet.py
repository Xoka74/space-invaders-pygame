from copy import copy

import config
from game_objects.game_object import GameObject
from repositories import images


class Bullet(GameObject):
    def __init__(self, pos, vel, shooter: GameObject):
        super().__init__(images.get('bullet'), pos, vel)
        self.shooter = shooter
        self.pos = copy(self.shooter.pos)

    def tick(self, level):
        super().tick(level)

        if self.pos.y <= 0 or self.pos.y >= config.SCREEN_HEIGHT:
            self.kill()
