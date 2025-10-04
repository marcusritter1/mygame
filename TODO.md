# TODO

## Bugs:

* if game was paused, camera moved is not triggered correctly and it takes a move of the camera until the map is redrawn, same for pause menu!

## Ideas:

* In full screen with large resolution in game I only get about 30 fps, how can I improve that?
  * render only what is displayed / that can fit on screen
  * render only stuff that has been changed, everything that has not been changed does not need to be redrawn every cycle of the game!

* fix WASD movement code - should be same logic as for mouse without near screen border detection...

* could have input via xbox controller

* how to put background audio for menu
* figure out how to put pyinstaller in path and make task executable for all systems, or create a simple .sh/bash script for building a executable of the game...
* map view in game screen, showing small version of entire map, with outline of current region shown on screen
* fog of war
* spawn point for enemy, algorithm to figure out position or use fix spawn points embedded in the map
* building menu, with a building that can be placed on the map, then building is displayed on map instead of previous texture, is registered in map object, saved on game save.
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
* if the set game screen resolution does not exist in system then the game crashes when clicking on game resolution selection

## Map related Questions:

* how to make isometric tiles, grid, textures? -> LIKE IN ANNO?
  * Anno 1602, 1503 used prerendered textures. The game does not use Iso rendering at all. It is a plain grid drawn to the screen.
  * It looks like it is very difficult to extract its textures as they are in the binaries of the game.
  * I could draw base layer of the map that is basically never changed by player as one big image, that would reduce rendering effort a lot. Other layers an animation can be drawn on top of that. This background image also needs only be updated very rarely most likely...
* tiles in class objects and load in game class

* zoom in and out of map - done
  * basic zoom is working but drops fps like crazy.
  * how to get high gps with zoom?

* how to rotate map and textures?

## Multiplayer:

* multiplayer menu to connect or join to a game lobby
* menu to create a new game lobby

## Map Editor

* one cool idea could be to build a separate map editor to build nice maps graphically with the tiles that I have fast...

## Game Engine

* Would it make sense to rewrite the game engine code more nicely in a directly compilable language like C++, Rust, C#, or else... to improve the game performance?
  * would also be possible then to create an executable directly
  * look for better integration with OpenGL, Vulkan, DirectX or another graphics library...
  * what about multi processing and threading support?

* how to utilize OpenGL in python to accelerate rendering with GPU?