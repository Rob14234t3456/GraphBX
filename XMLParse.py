import xml.etree.ElementTree as ElementTree
from Graphs import Graph, erdos_renyi_model_generation, ngon_generation, hypercube_generation
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


def parse_xml_graph(directory: str) -> Graph:
    # parses the XML graph file at directory into a graph object

    g = Graph()
    tree = ElementTree.parse(directory)
    vertices = tree.getroot().findall('vertex')

    # first add all vertices
    for v in vertices:
        g.add_vertex(eval(v.text))

    # then add edges
    for v in vertices:
        neighbours = v.findall('neighbour')
        for u in neighbours:
            g.add_edge(eval(v.text), eval(u.text))

    return g


def parse_xml_graph_coordinates(directory: str) -> dict:
    # parses the XML coordinate graph file at directory into a coordinate dict

    coords = dict()
    tree = ElementTree.parse(directory)
    vertices = tree.getroot().findall('vertex')

    # first add all vertices
    for v in vertices:
        c = v.findall('coordinate')[0]
        coords[eval(v.text)] = eval(c.text)

    return coords


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

