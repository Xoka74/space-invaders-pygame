import copy
import random
import sys

import pygame
from pygame import Vector2, mixer

import config
from controls import Button
from game_objects import Invader, Player, Bullet, Level, OtherBunker
from levels import levels
from repositories import sounds, images

pygame.init()

screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
pygame.display.set_caption(config.GAME_TITLE)


def quit_game():
    pygame.quit()
    sys.exit()


def render(game_object):
    screen.blit(game_object.sprite, game_object.pos)


def main_menu():
    play_button = Button('PLAY', pos=(config.SCREEN_WIDTH / 2, 100),
                         fontsize=36,
                         colors='white on black',
                         hover_colors="white on black", )
    quit_button = Button('QUIT', pos=(config.SCREEN_WIDTH / 2, 200),
                         fontsize=36,
                         colors='white on black',
                         hover_colors="white on black", )

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
                         colors='white on black',
                         hover_colors='white on black')

    buttons.add(back_button)
    local_levels = levels()

    for i in range(len(local_levels)):
        level = local_levels[i]
        button = Button(f'Level {level.name}', pos=(config.SCREEN_WIDTH / 2, 50 + i * 100),
                        fontsize=36,
                        colors='white on black',
                        hover_colors="white on black", )

        buttons.add(button)

    while True:
        screen.fill('black')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if back_button.clicked():
            return

        buttons_list = list(buttons)

        for i in range(1, len(buttons_list)):
            if buttons_list[i].clicked():
                play_level(levels()[i - 1])

        buttons.draw(screen)
        buttons.update()
        pygame.display.update()


def play_level(level: Level):
    TRIGGER_MYSTERY_SHIP, t = pygame.USEREVENT + 1, 1000
    bullet_image = images.get('bullet')
    pygame.time.set_timer(TRIGGER_MYSTERY_SHIP, t)
    font = pygame.font.Font('freesansbold.ttf', 20)

    bullet_sound = sounds.get('bullet')
    explosion_sound = sounds.get('explosion')
    background_sound = sounds.get('background')
    bunkers = pygame.sprite.Group()
    bunker = OtherBunker(images.get('bunker_default'), Vector2(0, 0), Vector2(0, 0))


    for b in [bunker]:
        bunkers.add(b)


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
                        bullet = Bullet(sprite=bullet_image, pos=Vector2(0, 0), vel=Vector2(0, -0.4),
                                        shooter=level.player)
                        level.bullets.append(bullet)
                        bullet_sound.play()
                        level.player.reload()
            if event.type == TRIGGER_MYSTERY_SHIP and not level.mystery_ship:
                level.start_mystery_ship()

            if event.type == pygame.KEYUP:
                level.player.vel.x = 0

        if level.mystery_ship:
            level.mystery_ship.update()
            render(level.mystery_ship)
            if not level.mystery_ship.started:
                level.end_mystery_ship()

        # bunkers
        for bullet in level.bullets:
            render(bullet)
            bullet.update()
        # for bunker in level.bunkers:
        #     bunker.kill()

        bunkers.update()
        bunkers.draw(screen)
        for b in bunkers:
            print(b.groups())

        # b.pos = level.bunkers[0].pos

        # for bunker in level.bunkers:
        #     bunker.update()

        # for bunker in level.bunkers:
        #     screen.set_at((int(bunker.pos.x), int(bunker.pos.y)), 255)
        #     render(bunker)
        #     bunker.update()

        if not list(level.invaders):
            pass

        for invader in level.invaders:
            invader.update()
            render(invader)

            if (invader.rect.collidelist([i.rect for i in level.bunkers])) != -1:
                return

            if invader.pos.x <= 50:
                invader.pos += Vector2(0, 50)
                invader.vel *= -1
            elif invader.pos.x >= config.SCREEN_WIDTH - 50:
                invader.pos += Vector2(0, 50)
                invader.vel *= -1

            if level.player.pos.x + 20 >= invader.pos.x >= level.player.pos.x - 20:
                if random.randint(1, 2000) == 1:
                    bullet = Bullet(sprite=bullet_image, pos=Vector2(0, 0), vel=Vector2(0, 0.4),
                                    shooter=invader)
                    level.bullets.append(bullet)

        render(level.player)
        level.player.update()

        for bullet in level.bullets:
            if isinstance(bullet.shooter, Invader):
                if bullet.rect.colliderect(level.player.rect):  # Invader -> Player
                    level.player.health -= 1
                    if level.player.health == 0:
                        game_over(level.score_val)
                        return

                    level.bullets.remove(bullet)

                elif (index := bullet.rect.collidelist([i.rect for i in level.bunkers])) != -1:  # Invader -> Bunker
                    bunker = level.bunkers[index]
                    if bunker.state == 4:
                        level.bunkers.pop(index)
                    else:
                        bunker.state += 1

                    level.bullets.remove(bullet)

            elif isinstance(bullet.shooter, Player):
                if (index := bullet.rect.collidelist([i.rect for i in level.invaders])) != -1:  # Player -> Invader
                    level.score_val += level.invaders[index].points
                    level.invaders.pop(index)
                    explosion_sound.play()
                    level.bullets.remove(bullet)

                elif level.mystery_ship and bullet.rect.colliderect(level.mystery_ship.rect):  # Player -> Mystery Ship
                    level.score_val += level.mystery_ship.points
                    level.end_mystery_ship()
                    pass

        score = font.render('Points: ' + str(level.score_val),
                            True, (255, 255, 255))
        screen.blit(score, (5, 5))

        health = font.render('Health: ' + str(level.player.health),
                             True, (255, 255, 255))
        screen.blit(health, (config.SCREEN_WIDTH - 150, 5))
        pygame.display.update()


def game_over(score_val):
    pass


if __name__ == '__main__':
    main_menu()
