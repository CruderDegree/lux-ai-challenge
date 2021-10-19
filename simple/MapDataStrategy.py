from lux.game_objects import CityTile
from lux.game_map import Cell
from lux.game import Game
from clusters.ClusterManager import ClusterManager
from clusters.Cluster import Cluster
from simple.lux.game_map import Position
import math

class MapDataStrategy():
    """
    Scan the map for tiles of interest and save them for later
    """

    def __init__(self, player_team : int, game_state : Game) -> None:
        self.resourceTiles: list[Cell] = []
        self.playerCityTiles: list[CityTile] = []
        self.map = game_state.map

        self.playerUnitsByPosition : dict = {}
        for unit in game_state.players[player_team].units:
            self.playerUnitsByPosition[unit.pos] = unit
        
        self.opponentUnitsByPosition : dict = {}
        for unit in game_state.players[(player_team + 1) % 2].units:
            self.opponentUnitsByPosition[unit.pos] = unit

        width, height = game_state.map.width, game_state.map.height
        for y in range(height):
            for x in range(width):
                cell = game_state.map.get_cell(x, y)
                if cell.has_resource():
                    self.resourceTiles.append(cell)
                    if cell.pos not in ClusterManager.clusterPositions:
                        newCluster : Cluster = Cluster(cell.pos, cell.resource, self.map)
                        ClusterManager.clusters += [newCluster]
                        ClusterManager.addClusterPositions(newCluster)
                if (cell.citytile != None) and (cell.citytile.team == player_team):
                    self.playerCityTiles.append(cell.citytile)

    def unitAtPosition(self, position : Position) -> bool:
        return position in self.playerUnitsByPosition.keys() or position in self.opponentUnitsByPosition.keys()
    
    def getClosestCityTile(self, position : Position) -> CityTile:
        smallestDistanceSoFar = math.inf
        closestCityTile = None
        for cityTile in self.playerCityTiles:
            if cityTile.pos.distance_to(position) < smallestDistanceSoFar:
                closestCityTile = cityTile
        return closestCityTile

    def unitCanMoveToPosition(self, position : Position) -> bool:
        cell = self.map.get_cell_by_pos(position)
        if cell.citytile is not None:
            return not self.unitAtPosition(position) and cell.citytile in self.playerCityTiles
        return not self.unitAtPosition(position)
            