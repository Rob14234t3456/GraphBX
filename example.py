from Graphs import *
import fpt
import GraphsRender

# 1 - network flows
network = Network()
network.add_vertices('A', 'B')
network.add_arc('S', 'A', weight=2)
network.add_arc('A', 'T', weight=2)
network.add_arc('A', 'B', weight=1)
network.add_arc('S', 'B', weight=1)
network.add_arc('B', 'T', weight=2)
f = network.max_flow()


# 2 - Ramsey Algorithm
graph = Graph()
graph.add_vertices(*[i for i in range(16)])
erdos_renyi_model_generation(graph, 0.6)

s = fpt.ramsey_algorithm(4, graph)


# 3 - shortest paths
f2 = graph.shortest_path(1, 2)


# 4 - Graph Rendering
GraphsRender.render_graph(graph, 1200, 1200, 0.7, 0.8)
