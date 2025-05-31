import pygame
import pygame_gui
import argparse

from menu import Menu
from game import Game
from settings import Settings
from game_settings import GameSettings
from game_enums import WindowMode
from util import get_current_resolution, get_possible_resolutions, detect_system, TargetSystem, detect_refresh_rate
from save_games import load_savegame
from win_screen import WinScreen
from lost_screen import LostScreen

def main():

    parser = argparse.ArgumentParser(description="My Isometric Game")
    parser.add_argument("--debug", action="store_true", help="Enable debug output.")
    parser.add_argument("--mapdebug", action="store_true", help="Enable debug visualizations for map.")
    parser.add_argument("--map", type=str, default="", help="Load the game with a specific map, e.g., 'quadratic_island'.")
    parser.add_argument("--fpscounter", action="store_true", help="Enable the FPS counter.")
    args = parser.parse_args()

    MAP_DEBUG = False
    MAP = ""
    FPS_COUNTER = False
    DEBUG = False

    if args.mapdebug:
        MAP_DEBUG = True
    if args.map:
        MAP = args.map
    if args.fpscounter:
        FPS_COUNTER = True
    if args.debug:
        DEBUG = True

    # detect the system OS
    OS = detect_system()
    if DEBUG:
        print("Running on: ", OS)

    if OS == TargetSystem.NONE:
        return 1

    # detect system refresh rate
    REFRESH_RATE = detect_refresh_rate(OS)
    if DEBUG:
        print("Refresh rate:", REFRESH_RATE)
    
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

    menu = Menu(screen, WIDTH, HEIGHT, FPS_COUNTER, REFRESH_RATE)
    settings = Settings(screen, WIDTH, HEIGHT, resolutions_list, game_settings, FPS_COUNTER, REFRESH_RATE)
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
                    game = Game(screen=screen, game_resolution=game_resolution, game_settings=game_settings, new_game=True, MAP_DEBUG=MAP_DEBUG, MAP=MAP, FPS_COUNTER=FPS_COUNTER, REFRESH_RATE=REFRESH_RATE)
                elif action == "settings":
                    in_menu = False
                    in_settings = True
                elif action == "load":
                    in_menu = False
                    loaded_save = load_savegame()
                    game = Game(screen=screen, game_resolution=game_resolution, game_settings=game_settings, new_game=False, game_stats=loaded_save.game_stats, MAP_DEBUG=MAP_DEBUG, MAP=MAP, FPS_COUNTER=FPS_COUNTER, REFRESH_RATE=REFRESH_RATE)
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
