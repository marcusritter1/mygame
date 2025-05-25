import pygame
import pygame_gui

from menu import Menu
from game import Game
from settings import Settings
from game_settings import GameSettings
from game_enums import WindowMode
from util import get_current_resolution, get_possible_resolutions
from save_games import load_savegame
from win_screen import WinScreen
from lost_screen import LostScreen

def main():

    game_name = "MyGame"
    game_settings = GameSettings()

    game_resolution = game_settings.resolution

    resolutions_list = get_possible_resolutions()

    # Load the .ico icon
    icon = pygame.image.load("icon.ico")

    pygame.init()

    WIDTH, HEIGHT = game_resolution[0], game_resolution[1]

    pygame.display.set_icon(icon)

    if game_settings.window_mode == WindowMode.FULL_SCREEN:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    elif game_settings.window_mode == WindowMode.WINDOWED:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
    elif game_settings.window_mode == WindowMode.BORDERLESS:
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)

    pygame.display.set_caption(game_name)
    manager = pygame_gui.UIManager((WIDTH, HEIGHT))

    menu = Menu(screen, WIDTH, HEIGHT)
    settings = Settings(screen, WIDTH, HEIGHT, resolutions_list, game_settings)
    win_screen = WinScreen(screen, WIDTH, HEIGHT)
    lost_screen = LostScreen(screen, WIDTH, HEIGHT)

    game = None
    running = True
    in_menu = True
    in_settings = False
    won = False
    lost = False

    while running:
        time_delta = pygame.time.Clock().tick(60) / 1000.0  # Frame rate

        if in_menu:
            menu.manager.update(time_delta)
            menu.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # X button triggers quit popup
                    running = False

                action = menu.handle_event(event)
                if action == "start":
                    in_menu = False
                    game = Game(screen=screen, game_resolution=game_resolution, game_settings=game_settings, new_game=True)
                elif action == "settings":
                    in_menu = False
                    in_settings = True
                elif action == "load":
                    in_menu = False
                    loaded_save = load_savegame()
                    game = Game(screen=screen, game_resolution=game_resolution, game_settings=game_settings, new_game=False, game_stats=loaded_save.game_stats)
                elif action == "exit":  # Directly quit, no popup
                    in_menu = False
                    running = False

        elif in_settings:
            settings.manager.update(time_delta)
            settings.draw()
            for event in pygame.event.get():
                action = settings.handle_event(event)
                if action == "back_to_menu":
                    in_settings = False
                    lost = False
                    won = False
                    in_menu = True

        elif won:
            win_screen.manager.update(time_delta)
            win_screen.draw()
            for event in pygame.event.get():
                action = win_screen.handle_event(event)
                if action == "back_to_menu":
                    in_settings = False
                    lost = False
                    won = False
                    in_menu = True

        elif lost:
            lost_screen.manager.update(time_delta)
            lost_screen.draw()
            for event in pygame.event.get():
                action = lost_screen.handle_event(event)
                if action == "back_to_menu":
                    in_settings = False
                    lost = False
                    won = False
                    in_menu = True

        else:  # In the game loop

            result = game.run()
            if result == "menu":
                in_settings = False
                lost = False
                won = False
                in_menu = True
            elif result == "exit":
                in_settings = False
                lost = False
                won = False
                running = False
            elif result == "game_won":
                won = True
                in_settings = False
                in_menu = False
            elif result == "game_lost":
                lost = True
                in_settings = False
                in_menu = False

    pygame.quit()

if __name__ == "__main__":
    main()
