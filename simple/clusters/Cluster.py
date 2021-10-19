from lux.game_map import Position, Cell, Resource
from simple.MapDataStrategy import MapDataStrategy
from simple.lux.game_map import DIRECTIONS, GameMap
import math

class Cluster():
    def __init__(self, initialPosition : Position, resource : Resource, map : GameMap) -> None:
        self.positions : list =  [initialPosition]
        self.resource : Resource = resource
        self.totalResources : int = resource.amount

        self._findAdjacentPositions(initialPosition, DIRECTIONS.CENTER, map)

    def _findAdjacentPositions(self, position : Position, direction : str, map : GameMap):
        """
        Searches for adjacent resources of the same kind in all directions except the one provided
        """
        directions = [DIRECTIONS.NORTH, DIRECTIONS.EAST, DIRECTIONS.SOUTH, DIRECTIONS.WEST]
        if direction != DIRECTIONS.CENTER:
            directions.remove(direction)
        
        for newDirection in directions:
            newPosition : Position = position.translate(newDirection, 1)
            newCell : Cell = map.get_cell_by_pos(newPosition)
            if newCell.resource == self.resource:
                self.positions += [newPosition]
                self.totalResources += newCell.resource.amount
                oppositeDirections = {
                    DIRECTIONS.NORTH : DIRECTIONS.SOUTH, 
                    DIRECTIONS.SOUTH : DIRECTIONS.NORTH,
                    DIRECTIONS.CENTER : DIRECTIONS.CENTER,
                    DIRECTIONS.EAST : DIRECTIONS.WEST,
                    DIRECTIONS.WEST : DIRECTIONS.EAST}
                self._findAdjacentPositions(newPosition, oppositeDirections[direction], map)

    def shortestDistanceToCluster(self, position : Position) -> int:
        distances = [position.distance_to(p) for p in self.positions]
        return min(distances)

    def nearestAdjClearCell(self, position : Position, map : GameMap) -> Position:
        directions = [DIRECTIONS.NORTH, DIRECTIONS.EAST, DIRECTIONS.SOUTH, DIRECTIONS.WEST]
        clearCellPositions = []
        for clusterPosition in self.positions:
            for direction in directions:
                cell = map.get_cell_by_pos(position.translate(direction, 1))
                if not cell.has_resource() and cell.citytile is None:
                    clearCellPositions.append(cell.pos)
        if clearCellPositions != []:
            return min([position.distance_to(p) for p in clearCellPositions])
        return None
    
    def getOptimalHarvestPosition(self, mapData : MapDataStrategy, position : Position, space_left):
        lowestDesireScore = math.inf 
        lowestDesireScoreIdx = 0
        for i in range(len(self.positions)):
            desireScore = self.getDesireScore(mapData, self.positions[i], position, space_left)
            if desireScore < lowestDesireScore:
                lowestDesireScoreIdx = i
        return self.positions[lowestDesireScoreIdx]
        

    def getDesireScore(self, mapData : MapDataStrategy, position : Position, workerPosition : Position, space_left):
        if mapData.unitAtPosition(position):
            return math.inf
        maxHarvestableResources = min(20, mapData.map.get_cell_by_pos(position).resource.amount)
        harvestableTiles = 1
        directions = [DIRECTIONS.NORTH, DIRECTIONS.EAST, DIRECTIONS.SOUTH, DIRECTIONS.WEST]
        for direction in directions:
            new_position = position.translate(direction, 1)
            new_cell = mapData.map.get_cell_by_pos(new_position)
            if not mapData.unitAtPosition(position) and new_cell.resource is not None:
                harvestableTiles += 1
                maxHarvestableResources = min(maxHarvestableResources, new_cell.resource.amount)
        maxHarvestPerTurn = harvestableTiles * maxHarvestableResources
        return maxHarvestPerTurn/space_left + workerPosition.distance_to(position)

