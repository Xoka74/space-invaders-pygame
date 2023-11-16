import sys
import pygame
import config
from Game import Game
from Level import Level
from controls import Button
from game_objects import Invader, Player
from levels import levels

pygame.init()
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
pygame.display.set_caption(config.GAME_TITLE)
local_levels = levels()


def quit_game():
    pygame.quit()
    sys.exit()




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
    game = Game(level, screen)
    game.start()
    return game.level.score_val


if __name__ == '__main__':
    main_menu()
