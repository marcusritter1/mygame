from datetime import datetime
import uuid
from uuid import UUID
import json

class SaveGame():

    def __init__(self, id: UUID = None, time: str = None, date: str = None, gold: int = 0) -> None:

        self.id = id
        self.time = time
        self.date = date
        
        # set the value saved in the save game
        self.gold = gold

        self.data = {}

    def generate_savegame_id(self) -> None:
        self.id = uuid.uuid4()

    def generate_savegame_timestamp(self) -> None:
        # get current time
        current_time = datetime.now()
        self.time = current_time.strftime("%H:%M:%S")
        # get current date
        self.date = datetime.now().strftime("%d.%m.%Y")

    def store_data_in_dict(self) -> None:
        self.data["id"] = str(self.id)
        self.data["date"] = self.date
        self.data["time"] = self.time
        self.data["gold"] = self.gold

    def save_savegame(self) -> None:
        self.generate_savegame_id()
        self.generate_savegame_timestamp()
        self.store_data_in_dict()
        try:
            with open("save_games/save_game_1.json", "w") as file:
                json.dump(self.data, file, indent=4)

        except (json.JSONDecodeError, FileNotFoundError, KeyError) as e:
            print(f"Error: {e}")


def load_savegame() -> SaveGame:
    try:
        with open("save_games/save_game_1.json", 'r') as file:
            data = json.load(file)
            return SaveGame(UUID(data["id"]), data["time"], data["date"], data["gold"])
        
    except Exception as e:
        print(f"Error reading the file: {e}")



save = SaveGame(gold=500)
save.save_savegame()

loaded_save = load_savegame()
print(str(loaded_save.id), loaded_save.time, loaded_save.date, loaded_save.gold)
