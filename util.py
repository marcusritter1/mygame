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