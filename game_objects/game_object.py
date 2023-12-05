import pygame
from pygame import Surface, Vector2


class GameObject(pygame.sprite.Sprite):
    def __init__(self, image: Surface, pos: Vector2, vel: Vector2):
        super().__init__()
        self.image = image
        self.pos = pos
        self.vel = vel
        self.rect = self.image.get_rect(center=self.pos)

    def tick(self, level):
        self.update()
        self.pos += self.vel
        self.rect.center = self.pos
