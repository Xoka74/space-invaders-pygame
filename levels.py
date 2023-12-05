import pygame
from pygame import Vector2

import config
from level import Level
from game_objects import Bunker, Invader, MysteryShip, Player
from repositories import images


def get_bunkers(amount):
    result = pygame.sprite.Group()
    bunker_image = images.get('bunker_default')
    bunker_width = bunker_image.get_width()
    offset = (config.SCREEN_WIDTH - amount * bunker_width) / (amount + 1)

    for i in range(amount):
        pos = Vector2(x=(offset + bunker_width / 2) * (i + 1),
                      y=config.SCREEN_HEIGHT - 125)
        bunker = Bunker(pos=pos,
                        vel=Vector2(0, 0),
                        state=0)
        result.add(bunker)
    return result


def get_invaders(amount, row_amount):
    result = pygame.sprite.Group()
    for i in range(row_amount):
        image = pygame.transform.scale_by(
            pygame.image.load(f'data/images/enemy_{i + 1}/0.png'), 3)

        invader_width = image.get_width()
        offset = (config.SCREEN_WIDTH - amount * invader_width) / (amount + 1)

        for j in range(amount):
            pos = Vector2(x=(offset + invader_width / 2) * (j + 1),
                          y=40 + 50 * (i + 1))
            vel = Vector2(0.1, 0)
            result.add(Invader(image, pos, vel, points=20))

    return result


def levels():
    return [
        Level('1',
              get_invaders(amount=1, row_amount=3),
              get_bunkers(4),
              Player(pos=Vector2(370, 523), vel=Vector2(0, 0), health=3,
                     reload_seconds=1),
              MysteryShip(Vector2(x=25, y=25), Vector2(0.35, 0),
                          duration=5,
                          points=200)),
        Level('2',
              get_invaders(amount=5, row_amount=3),
              get_bunkers(3),
              Player(pos=Vector2(370, 523), vel=Vector2(0, 0), health=2,
                     reload_seconds=1),
              MysteryShip(Vector2(x=25, y=25), Vector2(0.35, 0),
                          duration=5,
                          points=200)),
        Level('3',
              get_invaders(amount=11, row_amount=3),
              get_bunkers(2),
              Player(pos=Vector2(370, 523), vel=Vector2(0, 0), health=1,
                     reload_seconds=1),
              MysteryShip(Vector2(x=25, y=25), Vector2(0.35, 0),
                          duration=5,
                          points=200))
    ]
