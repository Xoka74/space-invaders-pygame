import random
import sys

import pygame
from pygame import Vector2

import config
from controls import Button
from game_objects import Invader, Player, Bullet, Level
from levels import levels
from repositories import sounds, images

pygame.init()

screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
pygame.display.set_caption(config.GAME_TITLE)
local_levels = levels()


def quit_game():
    pygame.quit()
    sys.exit()


def render(game_object):
    screen.blit(game_object.image, game_object.rect)


def main_menu():
    play_button = Button('PLAY', pos=(config.SCREEN_WIDTH / 2, 100),
                         fontsize=36,
                         colors='white on black', )
    quit_button = Button('QUIT', pos=(config.SCREEN_WIDTH / 2, 200),
                         fontsize=36,
                         colors='white on black', )

    buttons = pygame.sprite.Group()
    buttons.add(play_button, quit_button)
    while True:
        screen.fill('black')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if play_button.clicked():
            levels_menu()
        elif quit_button.clicked():
            quit_game()
        buttons.draw(screen)
        buttons.update()

        pygame.display.update()


def levels_menu():
    buttons = pygame.sprite.Group()
    back_button = Button('BACK', pos=(40, 40),
                         fontsize=36,
                         colors='white on black', )

    buttons.add(back_button)

    for i in range(len(local_levels)):
        level = local_levels[i]
        button = Button(f'Level {level.name} | High score: {level.high_score}',
                        pos=(config.SCREEN_WIDTH / 2, 50 + i * 100),
                        fontsize=36,
                        colors='white on black', )

        buttons.add(button)

    while True:
        screen.fill('black')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        if back_button.clicked():
            return

        buttons_list = list(buttons)

        for i in range(1, len(buttons_list)):
            button = buttons_list[i]
            if button.clicked():
                level = levels()[i - 1]
                base_level = local_levels[i - 1]
                score_val = play_level(level)
                if base_level.high_score >= score_val:
                    continue

                base_level.high_score = score_val
                button.set_text(f'Level {base_level.name} | High score: {base_level.high_score}')

        buttons.draw(screen)
        buttons.update()
        pygame.display.update()


def play_level(level: Level):
    TRIGGER_MYSTERY_SHIP, t = pygame.USEREVENT + 1, 10000
    bullet_image = images.get('bullet')
    pygame.time.set_timer(TRIGGER_MYSTERY_SHIP, t)
    font = pygame.font.Font('freesansbold.ttf', 20)

    bullet_sound = sounds.get('bullet')
    explosion_sound = sounds.get('explosion')
    background_sound = sounds.get('background')

    while True:

        # RGB
        screen.fill('black')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    level.player.vel.x = -0.4
                if event.key == pygame.K_RIGHT:
                    level.player.vel.x = 0.4

                if event.key == pygame.K_SPACE:
                    if not level.player.reloading:
                        bullet = Bullet(pos=Vector2(0, 0), vel=Vector2(0, -0.4), shooter=level.player)
                        level.bullets.add(bullet)
                        bullet_sound.play()
                        level.player.reload()

            if event.type == TRIGGER_MYSTERY_SHIP and not level.mystery_ship.started:
                level.mystery_ship.start()

            if event.type == pygame.KEYUP:
                level.player.vel.x = 0

        if level.mystery_ship.started:
            level.mystery_ship.update()
            render(level.mystery_ship)

        level.bullets.update()
        level.bullets.draw(screen)

        level.bunkers.update()
        level.bunkers.draw(screen)

        if not list(level.invaders):
            return level.score_val

        for invader in level.invaders:
            invader.update()
            render(invader)

            if (invader.rect.collidelist([i.rect for i in level.bunkers])) != -1:
                return level.score_val

            if invader.pos.x <= 50:
                invader.pos += Vector2(0, 50)
                invader.vel *= -1
            elif invader.pos.x >= config.SCREEN_WIDTH - 50:
                invader.pos += Vector2(0, 50)
                invader.vel *= -1

            if level.player.pos.x + 20 >= invader.pos.x >= level.player.pos.x - 20:
                if random.randint(1, 2000) == 1:
                    bullet = Bullet(image=bullet_image, pos=Vector2(0, 0), vel=Vector2(0, 0.4),
                                    shooter=invader)
                    level.bullets.add(bullet)

        render(level.player)
        level.player.update()

        for bullet in level.bullets:
            if isinstance(bullet.shooter, Invader):
                if bullet.rect.colliderect(level.player.rect):  # Invader -> Player
                    level.player.health -= 1
                    if level.player.health == 0:
                        return level.score_val

                    level.bullets.remove(bullet)

                elif (index := bullet.rect.collidelist([i.rect for i in level.bunkers])) != -1:  # Invader -> Bunker
                    bunker = list(level.bunkers)[index]
                    if bunker.state == 4:
                        level.bunkers.remove(bunker)
                    else:
                        bunker.state += 1

                    level.bullets.remove(bullet)

            elif isinstance(bullet.shooter, Player):
                if (index := bullet.rect.collidelist([i.rect for i in level.invaders])) != -1:  # Player -> Invader
                    invader = list(level.invaders)[index]
                    level.score_val += invader.points
                    level.invaders.remove(invader)
                    explosion_sound.play()
                    level.bullets.remove(bullet)

                elif level.mystery_ship and bullet.rect.colliderect(level.mystery_ship.rect):  # Player -> Mystery Ship
                    if level.mystery_ship.started:
                        level.score_val += level.mystery_ship.points
                        level.mystery_ship.end()

        score = font.render(f'Points: {level.score_val}',
                            True, (255, 255, 255))
        screen.blit(score, (5, 5))

        health = font.render(f'Health: {level.player.health}',
                             True, (255, 255, 255))
        screen.blit(health, (config.SCREEN_WIDTH - 150, 5))
        pygame.display.update()


if __name__ == '__main__':
    main_menu()
