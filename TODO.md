# TODO

## Ideas:

* how to put background audio for menu
* figure out how to put pyinstaller in path and make task executable for all systems, or create a simple .sh/bash script for building a executable of the game...
* map view in game screen, showing small version of entire map, with outline of current region shown on screen 
* fog of war
* spawn point for enemy, algorithm to figure out position or use fix spawn points embedded in the map
* building menu, with a building that can be placed on the map, then building is displayed on map instead of previous texture, is registered in map object, saved on game save.
* add a basic loose or win condition to the game, win when gold > 1000, loose if it is < -300.
* add a tool to the building menu to remove a building, again map needs to be updated 
* how to add animations to the map, like a water animation for the ocean to make it look like waves or flowing or a tree that is moving in the wind.
* objects that make up more than one tile. design a house 2.0 that uses 2x2 tiles and registers a click on it on each of its tiles
* turn the camera by a fix angle, e.g., 90° intervals or is it possible to turn it freely?
* basic game ai like an animal moving around, e.g. a wild boar, collision detection, does not hit go on ocean tiles for example 
* create more types of tiles, e.g., different tree and vegetation tiles, then find algorithm to randomly generate forests on the map, I don't want to build super detailed maps by hand 
* different types of background sounds: music, sound effects, menu option to turn them on off, set volume separately 

## UI & Menus

* have a in game stats window that show per minuete stats of game, e.g., gold income positive or negative atm...
* Have a menu for saving a game, where one can write savegame name and save it or even override existing savegame
* similar menu for loading save game where you can see all existing save games by date, time, and name, select one and load it, maybe even delete one...

## Map related Questions:

* how to make isometric tiles, grid, textures? -> LIKE IN ANNO?
* tiles in class objects and load in game class
* zoom in and out of map?
* when in fullscreen and the game res is smaller than screen resolution game still scrolls around even it is not necessary...
    * ideally game would also be centered for this scenario.

## Multiplayer:

* multiplayer menu to connect or join to a game lobby
* menu to create a new game lobby 

## Engie

* how to utilize OpenGL in python to accelerate rendering with GPU?
* isometrics:
    * pygame does not support z-order, so the last element drawn is always on top...
    * https://www.youtube.com/watch?v=gE2gTCwLdFM
    * https://www.youtube.com/watch?v=QpW6kC75aUA

    ```
    import pygame

    # Initialize pygame
    pygame.init()

    # Constants
    TILE_WIDTH = 64
    TILE_HEIGHT = 32
    MAP_WIDTH = 10
    MAP_HEIGHT = 10
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    # Create screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Load tile texture
    tile_img = pygame.image.load("tile.png").convert_alpha()

    # Convert grid coordinates to isometric
    def cart_to_iso(x, y):
        iso_x = (x - y) * TILE_WIDTH // 2 + SCREEN_WIDTH // 2
        iso_y = (x + y) * TILE_HEIGHT // 2
        return iso_x, iso_y

    # Game loop
    running = True
    while running:
        screen.fill((50, 50, 50))  # Background color

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw map
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                iso_x, iso_y = cart_to_iso(x, y)
                screen.blit(tile_img, (iso_x, iso_y))

        pygame.display.flip()

    pygame.quit()

    ```