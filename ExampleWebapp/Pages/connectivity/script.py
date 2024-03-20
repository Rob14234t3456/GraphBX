import Graphs
import XMLParse
from GraphsRender import generate_circle_coordinates

# create a graph for the connectivity page

graph = Graphs.Graph()
graph.add_vertices(1)

while graph.connected:
    graph = Graphs.erdos_renyi_model_generation(12, 0.15)

coords = generate_circle_coordinates(graph, 1000, 1000, 0.8)
XMLParse.parse_graph_coords(graph, coords, 'Pages/connectivity/graph_data.xml')
