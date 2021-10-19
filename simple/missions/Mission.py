from lux.game_objects import Unit
from Task import Task
from ActionTypes import *
from clusters.Cluster import Cluster
from simple.MapDataStrategy import MapDataStrategy
from simple.lux.game_map import GameMap, Position
from simple.missions.MissionTypes import *

class Mission:
    def __init__(self, missiontype : str, unit : Unit, cluster : Cluster, mapData : MapDataStrategy) -> None:
        self.type : str = missiontype
        self.unit : Unit = unit
        self.tasks : "list[Task]" = []
        self.targetCluster : Cluster = cluster

        self.updateMissionTasks(mapData)

    def updateMissionTasks(self, mapData : MapDataStrategy) -> None:
        map = mapData.map
        if self.type == CLAIM_CLUSTER:
            destination : Position = self.targetCluster.nearestAdjClearCell(self.unit.pos, map)
            self.tasks.append(Task(destination, SETTLE))
        elif self.type == SETTLE_CLUSTER:
            destination = self.targetCluster.nearestAdjClearCell(self.unit.pos, map)
            if destination is not None:
                self.tasks.append(Task(destination, SETTLE))
        elif self.type == MAINTAIN_CLUSTER:
            if self.unit.get_cargo_space_left > 0:
                destination : Position = self.targetCluster.getOptimalHarvestPosition(mapData, self.unit.pos, self.unit.get_cargo_space_left)
                self.tasks.append(Task(destination, TRAVEL))
            else:
                self.tasks.append(Task(mapData.getClosestCityTile(self.unit.pos), TRAVEL))
