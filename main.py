import pygame
import pygame_menu
from levels import load_levels
from game import Game
from persistence import HighScoreRepository, HighScore
from repositories import ImageRepository
from settings import Settings

pygame.init()
screen = pygame.display.set_mode((Settings.SCREEN_WIDTH,
                                  Settings.SCREEN_HEIGHT))
pygame.display.set_caption('Space invaders')
repo = HighScoreRepository('data/high_scores.json')
images = ImageRepository('data/images')
name = 'User123'


def name_change(new):
    global name
    name = new


def level_menu():
    level_menu = pygame_menu.Menu('Levels', Settings.SCREEN_WIDTH,
                                  Settings.SCREEN_HEIGHT)
    for i in range(len(load_levels(images))):
        level = load_levels(images)[i]
        level_menu.add.button(level.name, start_level, i)
    return level_menu


def update_leaderboards(menu):
    menu.clear()
    for level_info in repo.get_all():
        menu.add.button(level_info.name,
                        align=pygame_menu.locals.ALIGN_LEFT)

        for high_score in sorted(level_info.high_scores,
                                 key=lambda x: x.value,
                                 reverse=True):
            menu.add.button(
                f'{high_score.name} - {high_score.value} points',
                align=pygame_menu.locals.ALIGN_LEFT) \
                .set_margin(40, 0)


leaderboards = pygame_menu.Menu('Leaderboards', Settings.SCREEN_WIDTH,
                                Settings.SCREEN_HEIGHT)
update_leaderboards(leaderboards)


def start_level(i):
    level = load_levels(images)[i]
    game = Game(level, screen)
    game.start()

    high_score = HighScore(name, game.level.player.points)
    repo.add_or_update_high_score(level.name, high_score)
    update_leaderboards(leaderboards)


main_menu = pygame_menu.Menu('Main menu', Settings.SCREEN_WIDTH,
                             Settings.SCREEN_HEIGHT)
main_menu.add.text_input('Name: ', default=name,
                         onchange=name_change, maxchar=15)
main_menu.add.button('Play', level_menu())
main_menu.add.button('Leaderboards', leaderboards)
main_menu.add.button('Quit', pygame_menu.events.EXIT)

while True:
    if main_menu.is_enabled():
        main_menu.update(pygame.event.get())
        main_menu.draw(screen)

    pygame.display.update()
