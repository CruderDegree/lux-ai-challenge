from lux.game import Game
from lux.constants import Constants
from MapDataStrategy import MapDataStrategy
from WorkerStrategy import WorkerStrategy
from CityTileStrategy import CityTileStrategy
from ErrorLogger import eprint

DIRECTIONS = Constants.DIRECTIONS
game_state = None

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

    mapDataStrategy = MapDataStrategy(player_team, game_state)

    for city_id, city in player.cities.items():
        for city_tile in city.citytiles:
            if city_tile.can_act():
                cityTileStrategy : CityTileStrategy = CityTileStrategy(city_tile, player, mapDataStrategy.playerCityTiles)
                eprint("City tile {} in city {} can act".format(city_tile.pos, city.cityid))
                actions.append(cityTileStrategy.decide_action())

    for unit in player.units:
        if unit.is_worker() and unit.can_act():
            eprint("Worker {} can act".format(unit.pos))
            workerStrategy : WorkerStrategy = WorkerStrategy(unit, player, mapDataStrategy)
            action = workerStrategy.decide_action()
            if action is not None:
                actions.append(action)

    # you can add debug annotations using the functions in the annotate object
    # actions.append(annotate.circle(0, 0))
    
    return actions