import sys

import pygame
from pygame.sprite import spritecollideany

import config
from game_objects import Invader
from level import Level


class Game:
    def __init__(self, level: Level, screen):
        self.level = level
        self.screen = screen
        self._running = False
        pygame.init()

    def on_start(self):
        self._running = True
        pygame.mixer.music.load("data/sounds/background.wav")
        pygame.mixer.music.set_volume(config.GAME_VOLUME)
        pygame.mixer.music.play(-1)

    def start(self):
        self.on_start()
        TRIGGER_MYSTERY_SHIP, t = pygame.USEREVENT + 1, 10000
        pygame.time.set_timer(TRIGGER_MYSTERY_SHIP, t)
        font = pygame.font.Font('freesansbold.ttf', 20)
        while self._running:
            # RGB
            self.screen.fill('black')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.level.player.vel.x = -0.4
                    if event.key == pygame.K_RIGHT:
                        self.level.player.vel.x = 0.4

                    if event.key == pygame.K_SPACE:
                        self.level.player.shoot(self.level)

                if event.type == TRIGGER_MYSTERY_SHIP and \
                        not self.level.ship.started:
                    self.level.ship.start()

                if event.type == pygame.KEYUP:
                    self.level.player.vel.x = 0

            if self.level.ship.started:
                self.level.ship.tick(self.level)
                self.render(self.level.ship)

            for bullet in self.level.bullets:
                bullet.tick(self.level)

            self.level.bullets.draw(self.screen)

            for bunker in self.level.bunkers:
                bunker.tick(self.level)

            self.level.bunkers.draw(self.screen)

            if not list(self.level.invaders) or \
                    not self.level.player.alive:
                self._running = False

            for invader in self.level.invaders:
                invader.tick(self.level)
                self.render(invader)

            self.render(self.level.player)
            self.level.player.tick(self.level)

            self.handle_collisions()

            score = font.render(f'Points: {self.level.score_val}',
                                True, (255, 255, 255))
            self.screen.blit(score, (5, 5))

            health = font.render(f'Health: {self.level.player.health}',
                                 True, (255, 255, 255))
            self.screen.blit(health, (config.SCREEN_WIDTH - 150, 5))
            pygame.display.update()

        self.on_stop()

    def on_stop(self):
        pygame.mixer.music.stop()

    def handle_collisions(self):
        if b := spritecollideany(self.level.player, self.level.bullets):
            if isinstance(b.shooter, Invader):
                self.level.player.on_invader_bullet_collision(b, self.level)

        if b := spritecollideany(self.level.ship, self.level.bullets):
            self.level.ship.on_bullet_collision(b, self.level)

        for bullet in self.level.bullets:
            if bunker := spritecollideany(bullet, self.level.bunkers):
                bunker.on_bullet_collision(bullet, self.level)
            elif invader := spritecollideany(bullet, self.level.invaders):
                invader.on_bullet_collision(bullet, self.level)

        for invader in self.level.invaders:
            if bunker := spritecollideany(invader, self.level.bunkers):
                bunker.on_invader_collision(invader, self.level)

    def render(self, game_object):
        self.screen.blit(game_object.image, game_object.rect)
