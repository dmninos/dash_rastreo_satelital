import osmnx as ox
from pyprojroot import here
from pathlib import Path

ROOT = Path(here())
GRAPH = ROOT.joinpath('components', 'route')
GRAPH_DATA = GRAPH.joinpath("Bogota_drive.graphml")

class Route:
    def __init__(self):
        self.__place = "Bogota, Colombia"

        if GRAPH_DATA.exists():
            self.G = ox.io.load_graphml(GRAPH_DATA)
        else:
            self.G = ox.graph_from_place(self.__place, network_type='drive')

    def get_route(self, start, end):
        origin = ox.nearest_nodes(self.G, start[1], start[0])
        destination = ox.nearest_nodes(self.G, end[1], end[0])
        return ox.shortest_path(self.G, origin, destination, weight='length')

    def coordinates(self, start, end):
        route = self.get_route(start, end)
        lons = [self.G.nodes[n]['x'] for n in route]
        lats = [self.G.nodes[n]['y'] for n in route]
        return list(zip(lats, lons))

if __name__ == "__main__":
    route = Route()
    print(route.coordinates([4.61543788101837, -74.10690307617189], [4.582585016393075, -74.09866333007814]))