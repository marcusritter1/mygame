# TODO

## Ideas:

* task to build executable
* task to build virtualenv from requirements.txt
* how to put background audio for menu
* figure out how to put pyinstaller in path and make task executable for all systems, or create a simple .sh/bash script for building a executable of the game...
* map view in game screen, showing small version of entire map, with outline of current region shown on screen 
* fog of war
* spawn point for enemy, algorithm to figure out position or use fix spawn points embedded in the map
* building menu, with a building that can be placed on the map, then building is displayed on map instead of previous texture, is registered in map object, saved on game save.
* option in game to save and load a game, how to save all changes of the running game, json files?
* option in Menu to load a saved game and start it
* introduce a basic game stat like a currency, the house building can give +10 gold every 10 seconds when game is running. stats need to be saved and loaded, consider amount of houses 
* add a basic loose or win condition to the game, win when gold > 1000, loose if it is < -300.
* add a tool to the building menu to remove a building, again map needs to be updated 
* how to add animations to the map, like a water animation for the ocean to make it look like waves or flowing or a tree that is moving in the wind.
* how to click on an object on the map like a house with the mouse to then do something? the entire tile should register the mouse click.
* objects that make up more than one tile. design a house 2.0 that uses 2x2 tiles and registers a click on it on each of its tiles
* game Menu for in game with options like save and load game, exit to main menu, some settings, and back to game 
* turn the camera by a fix angle, e.g., 90° intervals or is it possible to turn it freely?
* basic game ai like an animal moving around, e.g. a wild boar, collision detection, does not hit go on ocean tiles for example 
* create more types of tiles, e.g., different tree and vegetation tiles, then find algorithm to randomly generate forests on the map, I don't want to build super detailed maps by hand 
* different types of background sounds: music, sound effects, menu option to turn them on off, set volume separately 

## Map related Questions:

* how to make isometric tiles, grid, textures? -> LIKE IN ANNO?
* move around map with arrow keys
* tiles in class objects and load in game class
* zoom in and out of map?
* when in fullscreen and the game res is smaller than screen resolution game still scrolls around even it is not necessary...
    * ideally game would also be centered for this scenario.

## Multiplayer:

* multiplayer menu to connect or join to a game lobby
* menu to create a new game lobby 