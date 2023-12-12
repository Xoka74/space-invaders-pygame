from copy import copy

from settings import Settings
from game_objects.game_object import GameObject


class Bullet(GameObject):
    def __init__(self, images, pos, vel, shooter: GameObject):
        super().__init__(images.get('bullet'), pos, vel)
        self.shooter = shooter
        self.pos = copy(self.shooter.pos)

    def tick(self, level):
        super().tick(level)

        if self.pos.y <= 0 or self.pos.y >= Settings.SCREEN_HEIGHT:
            self.kill()
