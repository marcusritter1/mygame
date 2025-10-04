import pygame
import sys
from enum import Enum
import subprocess
import re
import os

class TargetSystem(Enum):
    WINDOWS = 1
    MAC = 2
    LINUX = 3
    NONE = 4

def detect_system() -> TargetSystem:
    target_system = None
    if sys.platform.startswith("win"):
        target_system = TargetSystem.WINDOWS
    elif sys.platform.startswith("linux"):
        target_system = TargetSystem.LINUX
    elif sys.platform == "darwin":
        target_system = TargetSystem.MAC
    else:
        target_system = TargetSystem.NONE
    return target_system

def detect_refresh_rate(OS: TargetSystem) -> int:
    REFRESH_RATE = 60
    if OS == TargetSystem.MAC:
        import Quartz
        main_display = Quartz.CGMainDisplayID()
        mode = Quartz.CGDisplayCopyDisplayMode(main_display)
        REFRESH_RATE = Quartz.CGDisplayModeGetRefreshRate(mode)
        return REFRESH_RATE
    elif OS == TargetSystem.WINDOWS:
        import win32api
        devmode = win32api.EnumDisplaySettings(None, win32api.ENUM_CURRENT_SETTINGS)
        REFRESH_RATE = devmode.DisplayFrequency
        return REFRESH_RATE
    elif OS == TargetSystem.LINUX:
        refresh_rate = detect_refresh_rate_linux()
        if refresh_rate is not None:
            return refresh_rate
        else:
            return REFRESH_RATE
    elif OS == TargetSystem.NONE:
        return REFRESH_RATE
    else:
        return REFRESH_RATE

def detect_refresh_rate_linux():
    if os.environ.get("WAYLAND_DISPLAY"):
        return get_refresh_rate_gnome_wayland()
    elif os.environ.get("DISPLAY"):
        return get_refresh_rate_xrandr() or get_refresh_rate_glxinfo()
    else:
        return None

def get_refresh_rate_xrandr():
    try:
        output = subprocess.check_output(['xrandr'], universal_newlines=True)
        match = re.search(r'(\d+\.\d+)\*', output)
        if match:
            return float(match.group(1))
    except Exception:
        pass
    return None

def get_refresh_rate_glxinfo():
    try:
        output = subprocess.check_output(['glxinfo'], universal_newlines=True)
        match = re.search(r'refresh rate:\s+(\d+)', output, re.IGNORECASE)
        if match:
            return int(match.group(1))
    except Exception:
        pass
    return None

def get_refresh_rate_gnome_wayland():
    try:
        output = subprocess.check_output(
            ['gsettings', 'get', 'org.gnome.desktop.interface', 'refresh-rate'],
            universal_newlines=True
        )
        return int(output.strip())
    except Exception:
        pass
    return None

def read_maps_from_folder(maps_path: str = "saved_maps/") -> list[str]:
    map_options = []
    for filename in os.listdir(maps_path):
        file_path = os.path.join(maps_path, filename)
        file_path = file_path.replace(".json", "")
        file_path = file_path.replace(maps_path, "")
        map_options.append(file_path)
    return map_options

def get_current_resolution() -> tuple[int, int]:
    pygame.init()
    info = pygame.display.Info()
    return (info.current_w, info.current_h)

def get_possible_resolutions() -> list[tuple[int, int]]:
    pygame.init()
    display_modes = pygame.display.list_modes()
    return display_modes if display_modes else []

def split_evenly(x: int) -> tuple[int, int]:
    a = (x // 2) + 1 if x % 2 != 0 else x // 2
    b = x - a
    return a, b

def cart_to_iso(x, y, tile_size, screen_width, screen_height, camera_x, camera_y, iso_map_width, iso_map_height, map_width_smaller_than_screen, map_height_smaller_than_screen, zoom):

    tile_size = tile_size * zoom

    if map_width_smaller_than_screen is True:
        iso_x = (x - y) * (tile_size // 2) + camera_x + (iso_map_width // 2) - (tile_size // 2) #// 2
    else:
        iso_x = (x - y) * (tile_size // 2) + camera_x #+ screen_width / 2 - (tile_size // 2) #// 2

    if map_height_smaller_than_screen is True:
        iso_y = (x + y) * (tile_size // 4) + camera_y - (iso_map_width // 4) - (tile_size // 4) # + screen_height // 4
    else:
        iso_y = (x + y) * (tile_size // 4) + camera_y #- (screen_height / 4) #- (tile_size*0.75) # + screen_height // 4

    return iso_x, iso_y

def screen_to_iso(mouse_x, mouse_y, tile_size, screen_width, screen_height, camera_x, camera_y):
    """
    Convert screen coordinates (mouse_x, mouse_y) to Cartesian tile coordinates (x, y).

    tile_size: The base size of a tile before transformation.
    screen_width, screen_height: Dimensions of the screen.
    camera_x, camera_y: Current camera offset.
    """
    cart_x = ((mouse_x - screen_width // 2 - camera_x) / (tile_size // 2) +
              (mouse_y - screen_height // 4 - camera_y) / (tile_size // 4)) / 2

    cart_y = ((mouse_y - screen_height // 4 - camera_y) / (tile_size // 4) -
              (mouse_x - screen_width // 2 - camera_x) / (tile_size // 2)) / 2

    return int(cart_x), int(cart_y)

def screen_to_iso2(mouse_x, mouse_y, tile_size, screen_width, screen_height, camera_x, camera_y):
    """
    Convert screen coordinates (mouse_x, mouse_y) to Cartesian tile coordinates (x, y).

    tile_size: The base size of a tile before transformation.
    screen_width, screen_height: Dimensions of the screen.
    camera_x, camera_y: Current camera offset.
    """
    
    cart_x = ((mouse_x - camera_x) / (tile_size // 2) +
              (mouse_y - camera_y) / (tile_size // 4)) / 2

    cart_y = ((mouse_y - camera_y) / (tile_size // 4) -
              (mouse_x - camera_x) / (tile_size // 2)) / 2

    return int(cart_x), int(cart_y)

def calculate_map_padding(game_screen_width, game_screen_height, texture_size):
    tiles_visible_horizontally = (game_screen_width // (texture_size // 2)) // 2
    tiles_visible_vertically = (game_screen_height // (texture_size // 4)) // 2
    return max(tiles_visible_horizontally, tiles_visible_vertically)
