import Graphs
import GraphsRender
import XMLParse

graph = XMLParse.parse_xml_graph("ExampleWebapp/Pages/shortest_paths/graph_data.xml")
coords = XMLParse.parse_xml_graph_coordinates("ExampleWebapp/Pages/shortest_paths/graph_data.xml")

canvas = GraphsRender.Canvas(1000, 1000)
GraphsRender.render_graph_coordinate(canvas, graph, 1000, 1000, coords, 30)
canvas.begin_mainloop()
