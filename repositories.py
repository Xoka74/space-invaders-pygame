from pygame.image import load
from pygame.transform import scale_by


class ImageRepository:

    def __init__(self, root):
        self.source = {
            'mystery_ship': scale_by(
                load(f'{root}/mystery_ship/0.png'), 4),
            'bunker_default': scale_by(load(f'{root}/bunker/0.png'), 5),
            'player': scale_by(load(f'{root}/ship/0.png'), 3),
            'bullet': scale_by(load(f'{root}/bullet/0.png'), 3),
        }

        for i in range(0, 3):
            self.source[f'enemy_{i + 1}'] = \
                scale_by(load(f'{root}/enemy_{i + 1}/0.png'), 3)
        for i in range(0, 5):
            self.source[f'bunker_{i}'] = \
                scale_by(load(f'{root}/bunker/{i}.png'), 5)

    def get(self, name):
        return self.source.get(name)
