from game_enums import WindowMode
import json

class GameSettings():
    
    def __init__(self) -> None:
        self.window_mode = None
        
        self.game_settings_save_file_path = "game_settings.json"
        
        self.load_window_mode_from_json(self.game_settings_save_file_path)
        print("self.window_mode:",self.window_mode)
        
    def set_window_mode(self, window_mode: WindowMode) -> None:
        self.window_mode = window_mode
        
    def load_window_mode_from_json(self, file_path: str) -> None:
        try:
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
                window_mode = data.get("graphics_settings", {}).get("window_mode", None)
                if window_mode == "FULL_SCREEN":
                    self.window_mode = WindowMode.FULL_SCREEN
                elif window_mode == "WINDOWED":
                    self.window_mode =  WindowMode.WINDOWED
                elif window_mode == "BORDERLESS":
                    self.window_mode = WindowMode.BORDERLESS
                else:
                    self.window_mode = WindowMode.WINDOWED
        except Exception as e:
            print(f"Error reading the file: {e}")
            self.window_mode = WindowMode.WINDOWED