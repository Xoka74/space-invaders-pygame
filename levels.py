import pygame
from pygame import Vector2

import config
from game_objects import Invader, Bunker, Level, Player
from repositories import images


def get_bunkers(amount):
    bunkers = []
    bunker_image = images.get('bunker_default')
    bunker_width = bunker_image.get_width()
    offset = (config.SCREEN_WIDTH - amount * bunker_width) / (amount + 1)

    for i in range(amount):
        pos = Vector2(x=(offset + bunker_width / 2) * (i + 1), y=config.SCREEN_HEIGHT - 125)
        bunker = Bunker(bunker_image, pos=pos,
                        vel=Vector2(0, 0),
                        state=0)
        bunkers.append(bunker)
    return bunkers


def get_invaders(amount, row_amount):
    invaders = []
    for i in range(row_amount):
        image = pygame.transform.scale_by(pygame.image.load(f'data/images/enemy_{i + 1}/0.png'), 3)

        invader_width = image.get_width()
        offset = (config.SCREEN_WIDTH - amount * invader_width) / (amount + 1)

        for j in range(amount):
            pos = Vector2(x=(offset + invader_width / 2) * (j + 1), y=40 + 50 * (i + 1))
            vel = Vector2(0.1, 0)
            invaders.append(Invader(image, pos, vel, points=20))
    return invaders


def levels():
    return [
        Level('1',
              get_invaders(amount=5, row_amount=3),
              get_bunkers(4),
              Player(sprite=images.get('player'), pos=Vector2(370, 523), vel=Vector2(0, 0), health=1,
                     reload_seconds=1), ),
        Level('2',
              get_invaders(amount=5, row_amount=3),
              get_bunkers(3),
              Player(sprite=images.get('player'), pos=Vector2(370, 523), vel=Vector2(0, 0), health=1,
                     reload_seconds=1), ),
        Level('3',
              get_invaders(amount=11, row_amount=3),
              get_bunkers(2),
              Player(sprite=images.get('player'), pos=Vector2(370, 523), vel=Vector2(0, 0), health=1,
                     reload_seconds=1), )
    ]
