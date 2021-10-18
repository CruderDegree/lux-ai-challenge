from lux.game_map import Position, Cell, Resource
from simple.lux.game_map import DIRECTIONS, GameMap

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
