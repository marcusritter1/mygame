# Python Game

The game can be run using **uv** package manager. Use the following commands to run the game:

```
uv venv gameenv
uv sync
uv run python main.py
```

Scale texture images: `ffmpeg -i grass.png -vf scale=50:50 grass_scaled.png`.


Since, the tiles I use at the moment are 32x32 the calculation from Cartesian to isometric coordinates needs to be adjusted.

```
iso_x = (x - y) * (tile_size // 2) + camera_x + screen_width // 2
iso_y = (x + y) * (tile_size // 4) + camera_y + screen_height // 4
```

Normally, here we would use `(tile_size // 2)` if the tiles would be more diamond shaped as normal (double height than width).
