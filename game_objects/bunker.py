from game_objects import Invader
from game_objects import GameObject
from repositories import images


class Bunker(GameObject):
    def __init__(self, pos, vel, state: int):
        super().__init__(images.get('bunker_default'), pos, vel)
        self.state = state

    def tick(self, level):
        self.image = images.get(f'bunker_{self.state}')

    def on_invader_collision(self, invader, level):
        invader.kill()
        self.kill()
        level.player.kill()

    def on_bullet_collision(self, bullet, level):
        if isinstance(bullet.shooter, Invader):
            if self.state == 4:
                self.kill()
            else:
                self.state += 1
            bullet.kill()
