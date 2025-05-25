# Python Game

The game can be run using **uv** package manager. Use the following commands to run the game:

```
uv venv gameenv
uv sync
uv run python main.py
```

Scale texture images: `ffmpeg -i grass.png -vf scale=50:50 grass_scaled.png`.
