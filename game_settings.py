from game_enums import WindowMode
import json

class GameSettings():

    def __init__(self) -> None:
        self.window_mode = None
        self.resolution = None
        self.texture_size = (0, 0)

        self.game_settings_save_file_path = "settings/game_settings.json"

        self.load_window_mode_from_json()
        self.load_resolution_from_json()
        self.load_texture_size()

    def load_texture_size(self) -> None:
        try:
            with open(self.game_settings_save_file_path, 'r') as json_file:
                data = json.load(json_file)
                texture_dimesions = data.get("game_settings", {}).get("texture_size", None)
                self.texture_size = (texture_dimesions["height"], texture_dimesions["width"])
        except Exception as e:
            print(f"Error reading the file: {e}")
            self.texture_size = (32, 32)

    def set_window_mode(self, window_mode: WindowMode) -> None:
        self.window_mode = window_mode

    def load_window_mode_from_json(self) -> None:
        try:
            with open(self.game_settings_save_file_path, 'r') as json_file:
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

    def save_window_mode_to_json(self) -> None:
        try:
            with open(self.game_settings_save_file_path, "r") as file:
                data = json.load(file)

            data["graphics_settings"]["window_mode"] = self.window_mode.value

            with open(self.game_settings_save_file_path, "w") as file:
                json.dump(data, file, indent=4)

        except (json.JSONDecodeError, FileNotFoundError, KeyError) as e:
            print(f"Error: {e}")

    def load_resolution_from_json(self) -> None:
        try:
            with open(self.game_settings_save_file_path, 'r') as json_file:
                data = json.load(json_file)
                resolution = data.get("graphics_settings", {}).get("resolution", None)
                self.resolution = (resolution[0], resolution[1])
        except Exception as e:
            print(f"Error reading the file: {e}")
            self.resolution = (800, 600)

    def save_resolution_to_json(self) -> None:
        try:
            with open(self.game_settings_save_file_path, "r") as file:
                data = json.load(file)

            data["graphics_settings"]["resolution"] = self.resolution

            with open(self.game_settings_save_file_path, "w") as file:
                json.dump(data, file, indent=4)

        except (json.JSONDecodeError, FileNotFoundError, KeyError) as e:
            print(f"Error: {e}")
