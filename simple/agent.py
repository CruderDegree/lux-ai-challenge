import math, sys
from lux.game import Game
from lux.game_map import Cell, RESOURCE_TYPES
from lux.constants import Constants
from lux.game_constants import GAME_CONSTANTS
from lux import annotate
from lux.game_objects import CityTile, Player, Unit

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

def worker_strategy(unit : Unit, player, resource_tiles : list, city_tile_tiles : list) -> str:
    closest_dist = math.inf
    closest_resource_tile = None
    if unit.get_cargo_space_left() > 0:
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
        if len(city_tile_tiles) < 2:
            return unit.build_city()
        # if unit is a worker and there is no cargo space left, and we have cities, lets return to them
        if len(player.cities) > 0:
            closest_dist = math.inf
            closest_city_tile = None
            for k, city in player.cities.items():
                for city_tile in city.citytiles:
                    dist = city_tile.pos.distance_to(unit.pos)
                    if dist < closest_dist:
                        closest_dist = dist
                        closest_city_tile = city_tile
            if closest_city_tile is not None:
                move_dir = unit.pos.direction_to(closest_city_tile.pos)
                return unit.move(move_dir)

def city_tile_strategy(city_tile : CityTile, player : Player, city_tile_tiles : list) -> str:
    if len(player.units) < len(city_tile_tiles):
        return city_tile.build_worker
    else:
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
    
    resource_tiles, city_tile_tiles = scan_game_map(player_team)

    # we iterate over all our units and do something with them
    for unit in player.units:
        if unit.is_worker() and unit.can_act():
            actions.append(worker_strategy(unit, player, resource_tiles, city_tile_tiles))
    for city_id, city in player.cities.items():
        for city_tile in city.citytiles:
            if city_tile.can_act():
                actions.append(city_tile_strategy(city_tile, player, city_tile_tiles))
    # you can add debug annotations using the functions in the annotate object
    # actions.append(annotate.circle(0, 0))
    
    return actions