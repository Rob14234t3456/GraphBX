from Graphs import *
import GraphsRender
from random import randint

"""" Some random examples - use debugger to inspect namespace and see all results
"""


# 1 - network flows
network = Network()
network.add_vertices('A', 'B')
network.add_arc('S', 'A', weight=2)
network.add_arc('A', 'T', weight=2)
network.add_arc('A', 'B', weight=1)
network.add_arc('S', 'B', weight=1)
network.add_arc('B', 'T', weight=2)
f = network.max_flow()


# 2 - Graph Embeddings
graph = hypercube_generation(3)
sgraph = ngon_generation(3)
print("3-cube is 3-gon free: {}".format(find_embeddings(graph, sgraph) == []))

# s = fpt.ramsey_algorithm(4, graph)


# 3 - shortest paths
f2 = graph.shortest_path(0, 7)

# generate a path subgraph from f2
graph_f2 = Graph()
graph_f2.add_vertices(*f2)
for i in range(len(f2)-1):
    graph_f2.add_edge(f2[i], f2[i+1])


# 4 - max cliques
graph_3 = erdos_renyi_model_generation(6, 0.5)
cliques = graph_3.max_cliques()

canvas = GraphsRender.Canvas(1200, 1200)
coords = GraphsRender.generate_circle_coordinates(graph_3, 1200, 1200, 0.8)
GraphsRender.render_graph_coordinate(canvas, graph_3, coords, 30)
for c in cliques:
    # generates a random colour and draws subgraph for each clique
    color = "#" + ("%02x" % randint(0, 255)) + ("%02x" % randint(0, 255)) + ("%02x" % randint(0, 255))
    GraphsRender.render_graph_coordinate_style(canvas, graph_3.induced_subgraph(c), 1200, 1200, coords, 30,
                                               color, 4, 15)
canvas.begin_mainloop()


# 5 - complement graphs
graph_4 = erdos_renyi_model_generation(8, 0.5)
graph_4_complement = graph_4.complement()
canvas = GraphsRender.Canvas(1200, 1200)
coords = GraphsRender.generate_circle_coordinates(graph_4, 1200, 1200, 0.8)
GraphsRender.render_graph_coordinate_style(canvas, graph_4, 1200, 1200, coords, 30,
                                           "red", 2, 10)
GraphsRender.render_graph_coordinate_style(canvas, graph_4_complement, 1200, 1200, coords, 30,
                                           "blue", 2, 10)
canvas.begin_mainloop()


# 6 - Hypercube paths
canvas = GraphsRender.Canvas(1200, 1200)
coords = GraphsRender.generate_circle_coordinates(graph, 1200, 1200, 0.8)
GraphsRender.render_graph_coordinate(canvas, graph, coords, 30)
GraphsRender.render_graph_coordinate_style(canvas, graph_f2, 1200, 1200, coords, 30, "blue", 2, 15)
canvas.begin_mainloop()
