import pygame

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

def cart_to_iso(x, y, tile_size, screen_width, screen_height, camera_x, camera_y, iso_map_width, iso_map_height, map_width_smaller_than_screen, map_height_smaller_than_screen):

    if map_width_smaller_than_screen is True:
        iso_x = (x - y) * (tile_size // 2) + camera_x + (iso_map_width // 2) - (tile_size // 2) #// 2
    else:
        iso_x = (x - y) * (tile_size // 2) + camera_x + screen_width - (tile_size // 2) #// 2

    if map_height_smaller_than_screen is True:
        iso_y = (x + y) * (tile_size // 4) + camera_y - (iso_map_width // 4) - (tile_size // 4) # + screen_height // 4
    else:
        iso_y = (x + y) * (tile_size // 4) + camera_y - (tile_size // 4) # + screen_height // 4

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

def calculate_map_padding(game_screen_width, game_screen_height, texture_size):
    tiles_visible_horizontally = (game_screen_width // (texture_size // 2)) // 2
    tiles_visible_vertically = (game_screen_height // (texture_size // 4)) // 2
    return max(tiles_visible_horizontally, tiles_visible_vertically)
