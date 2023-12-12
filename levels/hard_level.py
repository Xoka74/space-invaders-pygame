from pygame import Vector2

from game_objects import Player, MysteryShip
from levels import Level
from levels.builders import LevelBuilder


class HardLevel(Level):

    def __init__(self, images):
        name = 'Hard'
        invaders = LevelBuilder.get_invaders(amount=11, row_amount=3,
                                             images=images)
        bunkers = LevelBuilder.get_bunkers(2, images=images)
        player = Player(pos=Vector2(370, 523), vel=Vector2(0, 0), health=1,
                        reload_seconds=1,
                        images=images)
        ship = MysteryShip(Vector2(x=25, y=25), Vector2(0.35, 0),
                           duration=5,
                           points=200,
                           images=images)
        super().__init__(name, invaders, bunkers, player, ship)
