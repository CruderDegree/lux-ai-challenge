from lux.game_map import Position

class Task:
    def __init__(self, destination : Position, action : str) -> None:
        self.destination : Position = destination
        self.action : str = action