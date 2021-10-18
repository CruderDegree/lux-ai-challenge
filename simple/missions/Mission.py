from lux.game_objects import Unit
from Task import Task
from ActionTypes import *
from clusters.Cluster import Cluster
from simple.lux.game_map import GameMap, Position
from simple.missions.MissionTypes import *

class Mission:
    def __init__(self, missiontype : str, unit : Unit, cluster : Cluster, map: GameMap) -> None:
        self.type : str = missiontype
        self.unit : Unit = unit
        self.tasks : "list[Task]" = []
        self.targetCluster : Cluster = cluster

        self.updateMissionTasks(map)

    def updateMissionTasks(self, map) -> None:
        if self.type == CLAIM_CLUSTER:
            destination : Position = self.targetCluster.nearestAdjClearCell(self.unit.pos, map)
            self.tasks.append(Task(destination, SETTLE))
