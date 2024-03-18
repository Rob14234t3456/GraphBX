from Graphs import hypercube_generation
import GraphsRender
from XMLParse import parse_graph_coords

"""" Generating and rendering a dimension 4 hypercube
"""

graph = hypercube_generation(4)
crds = GraphsRender.generate_circle_coordinates(graph, 1000, 1000, 0.8)
parse_graph_coords(graph, crds, "ExampleWebapp/index_demo_graph.xml")

canvas = GraphsRender.Canvas(1000, 1000)
GraphsRender.render_graph_coordinate(canvas, graph, 1000, 1000, crds, 30)
canvas.begin_mainloop()
