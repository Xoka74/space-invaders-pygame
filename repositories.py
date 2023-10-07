import pygame
from pygame import mixer


class ImageRepository:

    def __init__(self):
        self.source = {
            'mystery_ship': pygame.transform.scale_by(pygame.image.load('data/images/mystery_ship/0.png'), 4),
            'bunker_default': pygame.transform.scale_by(pygame.image.load('data/images/bunker/0.png'), 5),
            'player': pygame.transform.scale_by(pygame.image.load('data/images/ship/0.png'), 3),
            'bullet': pygame.transform.scale_by(pygame.image.load('data/images/bullet/0.png'), 3),
        }

        for i in range(0, 5):
            self.source[f'bunker_{i}'] = pygame.transform.scale_by(pygame.image.load(f'data/images/bunker/{i}.png'), 5)

    def get(self, name):
        return self.source.get(name)


class SoundRepository:
    def __init__(self):
        mixer.init()
        self.source = {
            'bullet': mixer.Sound('data/sounds/bullet.wav'),
            'background': mixer.Sound('data/sounds/background.wav'),
            'explosion': mixer.Sound('data/sounds/explosion.wav')
        }
        for k, v in self.source.items():
            v.set_volume(0.25)

    def get(self, name):
        return self.source.get(name)


images = ImageRepository()
sounds = SoundRepository()
