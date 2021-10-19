from lux.game_objects import Unit
from simple.agent import DIRECTIONS
from ErrorLogger import eprint
from MapDataStrategy import MapDataStrategy
from missions.Task import Task
from missions.ActionTypes import *

class WorkerStrategy():
    """
    Strategy used by a single worker
    """

    def __init__(self, worker : Unit, task : Task, mapData : MapDataStrategy) -> str:
        self.worker : Unit = worker
        self.task : Task = task
        self.mapData : MapDataStrategy = mapData

        if worker.pos != task.destination:
            return self.decideMoveAction()
        else:
            if self.task.action == SETTLE:
                return self.worker.build_city()
            return None
    
    def decideMoveAction(self) -> str:
        directions = [DIRECTIONS.NORTH, DIRECTIONS.EAST, DIRECTIONS.SOUTH, DIRECTIONS.WEST]
        current_distance = self.worker.pos.direction_to(self.task.destination)
        for direction in directions:
            newPos = self.worker.pos.translate(direction, 1)
            if newPos.distance_to(self.task.destination) < current_distance and self.mapData.unitCanMoveToPosition(newPos):
                return direction
        return None