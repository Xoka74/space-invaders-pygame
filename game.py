import sys

import pygame
from pygame.sprite import spritecollideany

from game_objects import Invader, Player
from levels.level import Level
from settings import Settings


class Game:
    def __init__(self, level: Level, screen):
        self.level = level
        self.screen = screen
        self.running = False
        self.TRIGGER_MYSTERY_SHIP, t = pygame.USEREVENT + 1, 10000
        pygame.time.set_timer(self.TRIGGER_MYSTERY_SHIP, t)
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.shoot_sound = pygame.mixer.Sound("data/sounds/bullet.wav")
        self.shoot_sound.set_volume(Settings.GAME_VOLUME)
        self.explosion_sound = \
            pygame.mixer.Sound("data/sounds/explosion.wav")
        self.explosion_sound.set_volume(Settings.GAME_VOLUME * 2)
        pygame.init()

    def _on_start(self):
        self.running = True
        pygame.mixer.music.load("data/sounds/background.wav")
        pygame.mixer.music.set_volume(Settings.GAME_VOLUME)
        pygame.mixer.music.play(-1)

    def start(self):
        self._on_start()
        while self.running:
            self.tick()
        self.stop()

    def _on_pause(self):
        pygame.mixer.music.pause()

    def _on_resume(self):
        pygame.mixer.music.unpause()

    def pause(self):
        self._on_pause()
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = False

            pause_hint = self.font.render('Pause', True, (255, 255, 255))

            self.screen.blit(pause_hint, (Settings.SCREEN_WIDTH / 2,
                                          Settings.SCREEN_HEIGHT / 2))
            pygame.display.update()
        self._on_resume()

    def tick(self):
        self.screen.fill('black')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(1)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.level.player.move_left()
                if event.key == pygame.K_RIGHT:
                    self.level.player.move_right()
                if event.key == pygame.K_SPACE:
                    if not self.level.player.reloading:
                        self.level.player.shoot(self.level)
                        self.shoot_sound.play()
                if event.key == pygame.K_ESCAPE:
                    self.pause()
            if event.type == self.TRIGGER_MYSTERY_SHIP and \
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
            self.stop()

        for invader in self.level.invaders:
            invader.tick(self.level)
            self.render(invader)

        self.render(self.level.player)
        self.level.player.tick(self.level)

        self.handle_collisions()

        score = self.font.render(f'Points: {self.level.player.points}',
                                 True, (255, 255, 255))
        self.screen.blit(score, (5, 5))

        health = self.font.render(f'Health: {self.level.player.health}',
                                  True, (255, 255, 255))
        self.screen.blit(health, (Settings.SCREEN_WIDTH - 150, 5))
        pygame.display.update()

    def stop(self):
        self._on_stop()

    def _on_stop(self):
        self.running = False
        pygame.mixer.music.stop()

    def handle_collisions(self):
        if b := spritecollideany(self.level.player, self.level.bullets):
            if isinstance(b.shooter, Invader):
                self.level.player.on_invader_bullet_collision(b)

        if inv := spritecollideany(self.level.player, self.level.invaders):
            self.level.player.on_invader_collision(inv)

        if b := spritecollideany(self.level.ship, self.level.bullets):
            self.level.ship.on_bullet_collision(b)

        for bullet in self.level.bullets:
            if bunker := spritecollideany(bullet, self.level.bunkers):
                bunker.on_bullet_collision(bullet)
            elif invader := spritecollideany(bullet, self.level.invaders):
                if isinstance(bullet.shooter, Player):
                    invader.on_bullet_collision(bullet)
                    self.explosion_sound.play()

    def render(self, game_object):
        self.screen.blit(game_object.image, game_object.rect)
