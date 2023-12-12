from game_objects import GameObject


class Bunker(GameObject):
    def __init__(self, pos, vel, state: int, images):
        super().__init__(images.get('bunker_default'), pos, vel)
        self.state = state
        self.images = images

    def tick(self, level):
        self.image = self.images.get(f'bunker_{self.state}')

    def on_bullet_collision(self, bullet):
        if self.state == 4:
            self.kill()
        else:
            self.state += 1
        bullet.kill()
