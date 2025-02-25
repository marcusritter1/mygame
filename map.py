import json
import numpy as np

class Map():
    
    def __init__(self):
        self.map_save_file_path = "saved_maps/saved_map_3.json"
        self.tile_grid = None
        
        self.load_map_from_json()
    
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