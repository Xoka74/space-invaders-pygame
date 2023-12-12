import pygame
from pygame import Vector2

from game_objects import Bunker, Invader
from settings import Settings


class LevelBuilder:
    @staticmethod
    def get_bunkers(amount, images):
        result = pygame.sprite.Group()
        bunker_image = images.get('bunker_default')
        bunker_width = bunker_image.get_width()
        offset = (Settings.SCREEN_WIDTH - amount * bunker_width) / \
                 (amount + 1)

        for i in range(amount):
            pos = Vector2(x=(offset + bunker_width / 2) * (i + 1),
                          y=Settings.SCREEN_HEIGHT - 125)
            bunker = Bunker(pos=pos,
                            vel=Vector2(0, 0),
                            state=0,
                            images=images)
            result.add(bunker)
        return result

    @staticmethod
    def get_invaders(amount, row_amount, images):
        result = pygame.sprite.Group()
        for i in range(row_amount):

            image = images.get(f'enemy_{i + 1}')
            invader_width = image.get_width()
            offset = (Settings.SCREEN_WIDTH - amount * invader_width) / \
                     (amount + 1)

            for j in range(amount):
                pos = Vector2(x=(offset + invader_width / 2) * (j + 1),
                              y=40 + 50 * (i + 1))
                vel = Vector2(0.1, 0)
                result.add(Invader(image, pos, vel, points=20, images=images))

        return result
