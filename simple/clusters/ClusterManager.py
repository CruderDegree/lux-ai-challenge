from Cluster import Cluster
from lux.game_map import Position
from lux.game_objects import Unit

class ClusterManager:
    clusters : "list[Cluster]" = []
    clusterPositions : "dict[Position : Cluster]" = {}
    clusterUnits : "dict[Unit : Cluster]" = {}

    def addClusterPositions(cluster : Cluster) -> None:
        for position in cluster.positions:
            ClusterManager.clusterPositions[position] = cluster
    
    def addUnitToCluster(unit : Unit, cluster : Cluster) -> None:
        ClusterManager.clusterUnits[unit] = cluster
    

