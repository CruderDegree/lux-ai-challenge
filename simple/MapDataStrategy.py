from lux.game_objects import CityTile
from lux.game_map import Cell
from lux.game import Game

class MapDataStrategy():
    """
    Scan the map for tiles of interest and save them for later
    """

    def __init__(self, player_team : int, game_state : Game) -> None:
        self.resourceTiles: list[Cell] = []
        self.playerCityTiles: list[CityTile] = []
        self.map = game_state.map

        width, height = game_state.map.width, game_state.map.height
        for y in range(height):
            for x in range(width):
                cell = game_state.map.get_cell(x, y)
                if cell.has_resource():
                    self.resourceTiles.append(cell)
                if (cell.citytile != None) and (cell.citytile.team == player_team):
                    self.playerCityTiles.append(cell.citytile)