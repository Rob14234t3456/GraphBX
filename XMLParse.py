import xml.etree.ElementTree as ElementTree
from Graphs import Graph, erdos_renyi_model_generation
import GraphsRender


def parse_dict(d: dict, directory: str):
    # parses a dict to a XML file and writes to path dir
    root = ElementTree.Element('mappings')

    for key in d.keys():
        emap = ElementTree.SubElement(root, 'map')

        ekey = ElementTree.SubElement(emap, 'key')
        ekey.text = repr(key)

        edat = ElementTree.SubElement(emap, 'data')
        edat.text = repr(d[key])

    tree = ElementTree.ElementTree(root)
    tree.write(directory)


def parse_xml_dict(directory: str) -> dict:
    # reads from directory and parses xml to an ElementTree, to a dict
    tree = ElementTree.parse(directory)
    mappings = tree.getroot()
    d = dict()

    for emap in mappings:
        ekey = emap.find('key')
        edat = emap.find('data')

        d[eval(ekey.text)] = eval(edat.text)

    return d


def parse_graph(g: Graph, directory: str):
    root = ElementTree.Element('vertices')

    for v in g.get_vertices():
        evertex = ElementTree.SubElement(root, 'vertex')
        evertex.text = repr(v)

        for u in g.neighbourhood(v):
            eneighbour = ElementTree.SubElement(evertex, 'neighbour')
            eneighbour.text = repr(u)

    tree = ElementTree.ElementTree(root)
    tree.write(directory)


def parse_graph_coords(g: Graph, coords: dict, directory: str):
    root = ElementTree.Element('vertices')

    for v in g.get_vertices():
        evertex = ElementTree.SubElement(root, 'vertex')
        evertex.text = repr(v)
        ecoord = ElementTree.SubElement(evertex, 'coordinate')
        ecoord.text = repr(coords[v])

        for u in g.neighbourhood(v):
            eneighbour = ElementTree.SubElement(evertex, 'neighbour')
            eneighbour.text = repr(u)

    tree = ElementTree.ElementTree(root)
    tree.write(directory)


graph = erdos_renyi_model_generation(7, 0.5)
crds = GraphsRender.generate_circle_coordinates(graph, 1000, 1000, 0.8)
parse_graph_coords(graph, crds, "ExampleWebapp/data.xml")

canvas = GraphsRender.Canvas(1000, 1000)
GraphsRender.render_graph_coordinate(canvas, graph, 1000, 1000, crds, 30)
GraphsRender.begin_mainloop(canvas)
