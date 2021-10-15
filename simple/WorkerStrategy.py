import math
from lux.game import Game
from lux.game_objects import Player, Unit, CityTile
from lux.constants import Constants
from lux.game_map import GameMap
from ErrorLogger import eprint
from MapDataStrategy import MapDataStrategy

class WorkerStrategy():
    """
    Strategy used by a single worker
    """

    def __init__(self, unit : Unit, player, mapDataStrategy : MapDataStrategy) -> None:
        self.unit : Unit = unit
        self.player : Player = player
        self.resourceTiles : list = mapDataStrategy.resourceTiles
        self.playerCityTiles : list = mapDataStrategy.playerCityTiles
        self.map : GameMap = mapDataStrategy.map
        
    def decide_action(self) -> str:
        closest_dist = math.inf
        closest_resource_tile = None
        if self.unit.get_cargo_space_left() > 0:
            eprint("Worker has cargo space left")
            # if the unit is a worker and we have space in cargo, lets find the nearest resource tile and try to mine it
            for resource_tile in self.resourceTiles:
                if resource_tile.resource.type == Constants.RESOURCE_TYPES.COAL and not self.player.researched_coal(): continue
                if resource_tile.resource.type == Constants.RESOURCE_TYPES.URANIUM and not self.player.researched_uranium(): continue
                dist = resource_tile.pos.distance_to(self.unit.pos)
                if dist < closest_dist:
                    closest_dist = dist
                    closest_resource_tile = resource_tile
            if closest_resource_tile is not None:
                return self.unit.move(self.unit.pos.direction_to(closest_resource_tile.pos))
        else:
            eprint("Worker has no cargo space left")
            if len(self.playerCityTiles) < 2:
                eprint("Fewer than 2 citytiles")
                return self.build_new_city_tile_strategy()

            # if unit is a worker and there is no cargo space left, and we have cities, lets return to them
            if len(self.player.cities) > 0:
                eprint("Worker {} moves towards nearest city tile".format(self.unit.pos))
                closest_dist = math.inf
                closest_city_tile : CityTile = None
                for k, city in self.player.cities.items():
                    for city_tile in city.citytiles:
                        dist = city_tile.pos.distance_to(self.unit.pos)
                        if dist < closest_dist:
                            closest_dist = dist
                            closest_city_tile = city_tile
                if closest_city_tile is not None:
                    eprint("Found closest city tile at {}".format(closest_city_tile.pos))
                    move_dir = self.unit.pos.direction_to(closest_city_tile.pos)
                    eprint("Worker {} moves in direction {}".format(self.unit.pos, move_dir))
                    return self.unit.move(move_dir)

    def build_new_city_tile_strategy(self) -> str:
        """ 
        Found a city on the nearest empty tile
        """
        if self.unit.can_build(self.map):
            eprint("Unit at {} builds a new citytile".format(self.unit.pos))
            return self.unit.build_city()
        else:
            eprint("Cannot build new citytile at position {}".format(self.unit.pos))
            x = self.unit.pos.x
            y = self.unit.pos.y
            neighbour_cells = [ self.map.get_cell(x + 1, y), 
                                self.map.get_cell(x - 1, y), 
                                self.map.get_cell(x, y + 1), 
                                self.map.get_cell(x, y - 1)]
            for cell in neighbour_cells:
                if not cell.has_resource():
                    eprint("Unit instead moves to {}".format(cell.pos))
                    return self.unit.move(self.unit.pos.direction_to(cell.pos))
        # Try moving to x+1 if all fails
        eprint("No empty cells nearby, moving to {} x+1".format(self.unit.pos))
        return self.unit.move(self.unit.pos.direction_to(self.map.get_cell(self.unit.pos.x + 1, self.unit.pos.y)))