from lux.game_objects import CityTile
from lux.game import Player
from ErrorLogger import eprint

class CityTileStrategy():
    """
    Strategy that an individual CityTile follows
    """
    def __init__(self, cityTile : CityTile, player : Player, playerCityTiles : list) -> None:
        self.cityTile : CityTile = cityTile
        self.player : Player = player
        self.playerCityTiles : list = playerCityTiles

    def decide_action(self) -> str:
        if len(self.player.units) < len(self.playerCityTiles):
            eprint("city tile at {} builds a worker".format(self.cityTile.pos))
            return self.cityTile.build_worker()
        else:
            eprint("city tile at {} researches".format(self.cityTile.pos))
            return self.cityTile.research()