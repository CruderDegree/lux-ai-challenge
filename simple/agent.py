import math, sys
from lux import game_map
from lux.game import Game
from lux.game_map import Cell, RESOURCE_TYPES, GameMap, Position
from lux.constants import Constants
from lux.game_constants import GAME_CONSTANTS
from lux import annotate
from lux.game_objects import CityTile, Player, Unit
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

DIRECTIONS = Constants.DIRECTIONS
game_state = None

def scan_game_map(player_team):
    width, height = game_state.map.width, game_state.map.height
    resource_tiles: list[Cell] = []
    citytile_tiles: list[CityTile] = []
    for y in range(height):
        for x in range(width):
            cell = game_state.map.get_cell(x, y)
            if cell.has_resource():
                resource_tiles.append(cell)
            if (cell.citytile != None) and (cell.citytile.team == player_team):
                citytile_tiles.append(cell.citytile)
    return resource_tiles, citytile_tiles

def worker_strategy(unit : Unit, player, resource_tiles : list, city_tile_tiles : list, map : GameMap) -> str:
    closest_dist = math.inf
    closest_resource_tile = None
    if unit.get_cargo_space_left() > 0:
        eprint("Worker has cargo space left")
        # if the unit is a worker and we have space in cargo, lets find the nearest resource tile and try to mine it
        for resource_tile in resource_tiles:
            if resource_tile.resource.type == Constants.RESOURCE_TYPES.COAL and not player.researched_coal(): continue
            if resource_tile.resource.type == Constants.RESOURCE_TYPES.URANIUM and not player.researched_uranium(): continue
            dist = resource_tile.pos.distance_to(unit.pos)
            if dist < closest_dist:
                closest_dist = dist
                closest_resource_tile = resource_tile
        if closest_resource_tile is not None:
            return unit.move(unit.pos.direction_to(closest_resource_tile.pos))
    else:
        eprint("Worker has no cargo space left")
        if len(city_tile_tiles) < 2:
            eprint("Fewer than 2 citytiles")
            return build_new_city_tile_strategy(unit, map)
        # if unit is a worker and there is no cargo space left, and we have cities, lets return to them
        if len(player.cities) > 0:
            eprint("Worker {} moves towards nearest city tile".format(unit.pos))
            closest_dist = math.inf
            closest_city_tile : CityTile = None
            for k, city in player.cities.items():
                for city_tile in city.citytiles:
                    dist = city_tile.pos.distance_to(unit.pos)
                    if dist < closest_dist:
                        closest_dist = dist
                        closest_city_tile = city_tile
            if closest_city_tile is not None:
                eprint("Found closest city tile at {}".format(closest_city_tile.pos))
                move_dir = unit.pos.direction_to(closest_city_tile.pos)
                eprint("Worker {} moves in direction {}".format(unit.pos, move_dir))
                return unit.move(move_dir)

def build_new_city_tile_strategy(unit : Unit, gameMap : GameMap) -> str:
    """ 
    Found a city on the nearest empty tile
    """
    if unit.can_build(gameMap):
        eprint("Unit at {} builds a new citytile".format(unit.pos))
        return unit.build_city()
    else:
        eprint("Cannot build new citytile at position {}".format(unit.pos))
        x = unit.pos.x
        y = unit.pos.y
        neighbour_cells = [ gameMap.get_cell(x + 1, y), 
                            gameMap.get_cell(x - 1, y), 
                            gameMap.get_cell(x, y + 1), 
                            gameMap.get_cell(x, y - 1)]
        for cell in neighbour_cells:
            if not cell.has_resource():
                eprint("Unit instead moves to {}".format(cell.pos))
                return unit.move(unit.pos.direction_to(cell.pos))
    # Try moving to x+1 if all fails
    eprint("No empty cells nearby, moving to {} x+1".format(unit.pos))
    return unit.move(unit.pos.direction_to(gameMap.get_cell(unit.pos.x + 1, unit.pos.y)))

def city_tile_strategy(city_tile : CityTile, player : Player, city_tile_tiles : list) -> str:
    if len(player.units) < len(city_tile_tiles):
        eprint("city tile at {} builds a worker".format(city_tile.pos))
        return city_tile.build_worker()
    else:
        eprint("city tile at {} researches".format(city_tile.pos))
        return city_tile.research()


def agent(observation, configuration):
    global game_state

    ### Do not edit ###
    if observation["step"] == 0:
        game_state = Game()
        game_state._initialize(observation["updates"])
        game_state._update(observation["updates"][2:])
        game_state.id = observation.player
    else:
        game_state._update(observation["updates"])
    
    actions = []

    ### AI Code goes down here! ### 
    player = game_state.players[observation.player]
    player_team : int = player.team   
    opponent = game_state.players[(observation.player + 1) % 2]
    
    eprint("Now player {}'s turn".format(player_team))
    eprint("Total research points: {}".format(player.research_points))

    resource_tiles, city_tile_tiles = scan_game_map(player_team)

    for city_id, city in player.cities.items():
        for city_tile in city.citytiles:
            if city_tile.can_act():
                eprint("City tile {} in city {} can act".format(city_tile.pos, city.cityid))
                actions.append(city_tile_strategy(city_tile, player, city_tile_tiles))
    # we iterate over all our units and do something with them
    for unit in player.units:
        if unit.is_worker() and unit.can_act():
            eprint("Unit is worker and can act")
            actions.append(worker_strategy(unit, player, resource_tiles, city_tile_tiles, game_state.map))
    # you can add debug annotations using the functions in the annotate object
    # actions.append(annotate.circle(0, 0))
    
    return actions