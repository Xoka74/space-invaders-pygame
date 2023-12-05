from pygame.image import load
from pygame.transform import scale_by


class ImageRepository:

    def __init__(self):
        self.source = {
            'mystery_ship': scale_by(
                load('data/images/mystery_ship/0.png'), 4),
            'bunker_default': scale_by(load('data/images/bunker/0.png'), 5),
            'player': scale_by(load('data/images/ship/0.png'), 3),
            'bullet': scale_by(load('data/images/bullet/0.png'), 3),
        }

        for i in range(0, 5):
            self.source[f'bunker_{i}'] = \
                scale_by(load(f'data/images/bunker/{i}.png'), 5)

    def get(self, name):
        return self.source.get(name)


images = ImageRepository()
