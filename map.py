import json
import numpy as np

class Map():

    def __init__(self):
        self.map_save_file_path = "saved_maps/quadratic_island.json"
        self.tile_grid = None
        self.num_houses = 0

        self.load_map_from_json()

        self.num_houses = np.count_nonzero(self.tile_grid == 3)

    def load_map_from_json(self) -> None:
        try:
            with open(self.map_save_file_path, 'r') as json_file:
                data = json.load(json_file)
                tile_grid = data.get("map", None)
                self.tile_grid = np.array(tile_grid)
        except Exception as e:
            print(f"Error reading the file: {e}")
            self.tile_grid = np.array([
                [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
            ])

    def get_map_tiles_width(self) -> int:
        return len(self.tile_grid[0])

    def get_map_tiles_height(self) -> int:
        return len(self.tile_grid)

    def get_num_houses(self) -> int:
        return self.num_houses
