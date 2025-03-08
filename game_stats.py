
class GameStats():

    def __init__(self, gold: int = 0):
        self.gold = gold

    def print_stats(self) -> None:
        print(self.gold)