from random import random
from MathOperations import hamming_distance, permutations


class BasicGraph:
    # class for graphs which shouldn't inherit methods that change the structure e.g. Trees should not
    # have a non-protected add_vertex method since this will disconnect them

    def __init__(self, *args):
        if len(args) == 0:
            self._graph = dict()
        elif len(args) == 1:
            # allows for defining a graph by a dict
            self._graph = args[0]

    def _add_vertex(self, v):
        self._graph[v] = set()

    def _add_vertices(self, *args):
        for v in args:
            self._add_vertex(v)

    def _add_edge(self, v1, v2):
        self._graph[v1].add(v2)
        self._graph[v2].add(v1)

    def _add_edges(self, *args):
        for e in args:
            self._add_edge(e[0], e[1])

    def adjacent(self, v1, v2):
        return v2 in self._graph[v1]

    def degree(self, v):
        return len(list(self.neighbourhood(v)))

    def get_vertices(self):
        return set(self._graph)

    def get_edges(self):
        # enumerate edges - set used to prevent reverses being counted
        # I use frozenset since set elements of a set cannot be mutable
        edges = {frozenset({v, u}) for v in self.get_vertices() for u in self.neighbourhood(v)}

        # convert to tuple format and return
        return {tuple(e) for e in edges}

    def neighbourhood(self, v):
        return set([u for u in self._graph if self.adjacent(v, u)])

    def path_exists(self, v1, v2):
        # returns true if a path exists between v1 and v2
        # scans the graph depth-first for shortest runtime

        def scan_vertex(vertex):
            explored.add(vertex)
            if vertex == v2:
                return True
            neighbours = self.neighbourhood(vertex) - explored
            for u in list(neighbours):
                scan_vertex(u)

        explored = {v1}
        scan_vertex(v1)
        return False

    def shortest_path(self, v1, v2):
        # uses a breadth-first traversal to find a shortest path between two vertices
        # def shortest_path(self, v1, v2):

        explored = set()
        visited = {v1}
        prev = dict()
        while v2 not in list(visited):
            for v in list(visited):
                for w in list(self.neighbourhood(v) - explored):
                    prev[w] = v
                    visited.add(w)
                explored.add(v)

        path = [v2]
        while v1 not in path:
            path.append(prev[path[-1]])
        return path

    # IN PROGRESS - NOT CURRENTLY WORKING
    def path_flow(self, v1, v2):
        # CURRENTLY DOES NOT WORK
        # uses a neat manipulation of network flows to find a path
        # far less efficient than breadth-first, but kinda cool

        aux_network = Network()
        aux_network.add_vertices(*list(self.get_vertices()))
        [aux_network.add_edge(e[0], e[1], 1) for e in self.get_edges()]
        aux_network.add_edge(v1, "S", 1)
        aux_network.add_edge(v2, "T", 1)
        flow = aux_network.max_flow()
        return flow

    def connected(self):
        def scan_vertex(vertex):
            explored.add(vertex)
            neighbours = self.neighbourhood(vertex) - explored
            for u in list(neighbours):
                scan_vertex(u)

        v = list(self._graph)[0]
        explored = {v}
        scan_vertex(v)
        return explored == set(self._graph)

    def get_spanning_tree(self, v):
        # returns a spanning tree, rooted at v, of the connected component containing v
        # uses Prim's algorithm
        spanning_tree = RootedTree(v)

        def scan_vertex(vertex):
            explored.add(vertex)
            neighbours = self.neighbourhood(vertex) - explored
            for u in list(neighbours):
                spanning_tree.add_child(vertex, u)
                scan_vertex(u)

        v = list(self._graph)[0]
        explored = {v}
        scan_vertex(v)
        return spanning_tree

    def induced_subgraph(self, vertices: set):
        # returns a new graph, the subgraph induced from vertex set given
        g = Graph()
        g.add_vertices(*vertices)
        for e in self.get_edges():
            if e[0] in vertices and e[1] in vertices:
                g.add_edge(e[0], e[1])
        return g

    # CURRENTLY MISSES SOME SINGLE-EDGE CLIQUES, UNSURE WHY
    def max_cliques(self):
        # uses the Bron-Kerbosch algorithm to compute a list of maximal cliques
        cliques = []

        def bk(r: list, p: list, x: list, clique_list: list) -> None:
            # R - current clique
            # P - potential expansions
            # X - explored vertices (excluding)
            # clique_set - outer set to be appended

            if len(p) == 0 and len(x) == 0:
                clique_list.append(set(r))

            for v in p:
                bk(r + [v], list(set(p).intersection(self.neighbourhood(v))),
                   list(set(x).intersection(self.neighbourhood(v))), clique_list)
                p.remove(v)
                x.append(v)

        bk([], list(self.get_vertices()), [], cliques)
        return cliques

    def complement(self):
        # returns a new graph with structure of the complement graph
        g = Graph()
        g.add_vertices(*self.get_vertices())
        g.add_edges(*[(u, v,) for u in self.get_vertices() for v in self.get_vertices()
                      if u != v and not self.adjacent(u, v)])
        return g


class RootedTree(BasicGraph):
    def __init__(self, root_name):
        # creates a basic graph with a single root vertex
        super().__init__({root_name: set()})
        self._children = {root_name: set()}
        self.root = root_name

    def add_child(self, parent, child):
        self._add_vertex(child)
        self._children[child] = set()
        self._add_edge(parent, child)
        self._children[parent].add(child)

    def is_child(self, parent, child):
        return child in self._children[parent]

    def get_children(self, parent):
        return self._children[parent]


class Graph(BasicGraph):
    def add_vertex(self, v):
        super()._add_vertex(v)

    def add_vertices(self, *args):
        super()._add_vertices(*args)

    def add_edge(self, v1, v2):
        super()._add_edge(v1, v2)

    def add_edges(self, *args):
        super()._add_edges(*args)


class DirectedGraph(Graph):
    def add_arc(self, v1, v2):
        self._graph[v1].add(v2)

    def add_arcs(self, *args):
        [self.add_arc(a[0], a[1]) for a in args]

    def get_arcs(self):
        return {(v, u) for v in self.get_vertices() for u in self.neighbourhood(v)}

    def arced(self, v1, v2):
        return v2 in self._graph[v1] or v1 in self._graph[v2]

    def arc_neighbourhood(self, v):
        return set([u for u in self._graph if self.arced(v, u)])

    def weakly_connected(self):
        def scan_vertex(vertex):
            explored.add(vertex)
            neighbours = self.arc_neighbourhood(vertex) - explored
            for u in list(neighbours):
                scan_vertex(u)

        for v in list(self._graph):
            explored = {v}
            scan_vertex(v)
            if not explored == set(self._graph):
                return False
        return True


class WeightedGraph(Graph):
    def __init__(self):
        super().__init__()
        self._c = dict()

    def add_edge(self, v1, v2, weight=0):
        super().add_edge(v1, v2)
        self._c[(v1, v2)] = weight
        self._c[(v2, v1)] = weight

    def get_weight(self, v1, v2):
        return self._c[(v1, v2)]

    # calculate a minimum path from v1 to v2 using Dijkstra's algorithm
    def shortest_path(self, v1, v2, key=None):
        if key is None:
            def key(x, y): self.get_weight(x, y)

        q = self.get_vertices()
        dist = {v: float('inf') for v in q}
        prev = {v: None for v in q}
        dist[v1] = 0

        while not q == set():
            u = min(*q, key=lambda x: dist[x])
            q.remove(u)
            for v in self.neighbourhood(u).intersection(q):
                alt = dist[u] + key(u, v)
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u

        path = [v2]
        while v1 not in path:
            path.append(prev[path[-1]])
        return path


class WeightedDirectedGraph(WeightedGraph, DirectedGraph):
    def add_arc(self, v1, v2, weight=0):
        super().add_arc(v1, v2)
        self._c[(v1, v2)] = weight

    def add_arcs(self, *args):
        [self.add_arc(a[0], a[1], weight=a[2]) if len(a) == 3 else self.add_arc(a[0], a[1]) for a in args]


class Network(WeightedDirectedGraph):
    def __init__(self, source='S', sink='T'):
        super().__init__()
        self._source = source
        self._sink = sink
        self.add_vertices(source, sink)

    def source(self):
        return self._source

    def sink(self):
        return self._sink

    def max_flow(self):
        # uses the greedy Ford-Fulkerson method to compute a maximal flow in O(V * max[aug_f]) time

        flow = NetworkFlow(self, {v: 0 for v in self.get_arcs()})
        gamma = float('inf')
        while gamma > 0:
            # find maximal augmenting path
            n = flow.residual_network()
            e = max(n.get_arcs(), key=lambda x: n.get_weight(x[0], x[1]))
            m = n.get_weight(e[0], e[1])
            p = n.shortest_path(n.source(), n.sink(), key=lambda x, y: m - n.get_weight(x, y))
            path = [(p[i+1], p[i]) for i in range(0, len(p)-1)]

            # augment network until best path is of 0 capacity
            gamma = min([n.get_weight(arc[0], arc[1]) for arc in path])
            [flow.change_flow(p[i], p[i - 1], gamma) for i in range(1, len(p)) if self.adjacent(p[i], p[i - 1])]
            [flow.change_flow(p[i], p[i - 1], -gamma) for i in range(1, len(p)) if not self.adjacent(p[i], p[i - 1])]
        return flow


class NetworkFlow:
    def __init__(self, network, arc_flow):
        self._network = network
        self._arc_flow = arc_flow

        # validate network flow
        # check vertex flow conservation is satisfied
        flow_in = {v: sum([arc_flow[(u, v)] for u in network.get_vertices() if v in network.neighbourhood(u)])
                   for v in network.get_vertices()}
        flow_out = {v: sum([arc_flow[(v, u)] for u in network.neighbourhood(v)])
                    for v in network.get_vertices()}
        for v in list(network.get_vertices() - {network.source(), network.sink()}):
            if not flow_in[v] == flow_out[v]:
                raise ValueError('Flow does not satisfy flow conservation at vertex {} with out flow {} '
                                 'and in flow {}.'.format(v, flow_out[v], flow_in[v])
                                 )

        # check arc flow does not exceed network arc capacity
        for arc in list(arc_flow):
            if arc_flow[arc] > network.get_weight(arc[0], arc[1]):
                raise ValueError('Flow exceeds capacity at arc {}'.format(arc))

    def flow(self, v1, v2):
        return self._arc_flow[(v1, v2)]

    def change_flow(self, v1, v2, w):
        self._arc_flow[(v1, v2)] += w

    def residual_network(self):
        n = Network()
        n.add_vertices(*list(self._network.get_vertices()))
        for arc in self._network.get_arcs():
            n.add_arc(arc[0], arc[1], weight=self._network.get_weight(arc[0], arc[1]) - self.flow(arc[0], arc[1]))
            n.add_arc(arc[1], arc[0], weight=self.flow(arc[0], arc[1]))
        return n

    def augmenting_path(self):
        n = self.residual_network()
        e = max(n.get_arcs(), key=lambda x: n.get_weight(x[0], x[1]))
        m = n.get_weight(e[0], e[1])
        return n.shortest_path(n.source(), n.sink(), key=lambda x, y: m - n.get_weight(x, y))


def find_embeddings(g1: Graph, g2: Graph):
    # in this library, an embedding is a mapping of the vertices of some graph g2, to the vertices
    # of another graph g1 such that (positive) adjacency between vertices of g2 is preserved.
    # for clarity, this means that arbitrary injections of the vertices of any graph to a complete
    # graph are embeddings, and the same is true for embeddings of the vertices of an empty graph to any graph.

    # v1 - enumerative method. Presumably a better algorithm can be found, similar to Bron-Kerbosch.
    # first, list vertices of g2 and assign their indices to a dict - this helps in permutation comprehension.
    g2l = list(g2.get_vertices())
    order = {g2l[i]: i for i in range(len(g2l))}

    embeddings = []
    # then, check each |V(g2)|-permutation of V(g1) for an embedding.
    for perm in permutations(list(g1.get_vertices()), len(g2.get_vertices())):
        if False not in [g1.adjacent(perm[order[e[0]]], perm[order[e[1]]]) for e in g2.get_edges()]:
            # if embedding is proper, generate the map and add to the list
            embeddings.append({g2l[i]: perm[i] for i in range(len(g2l))})

    return embeddings


def erdos_renyi_model_generation(n: int, p: float):
    # generate a random graph with n vertices and edge probability p
    g = Graph()
    g.add_vertices(*[i for i in range(n)])

    possible_edges = {frozenset({v, u}) for v in g.get_vertices() for u in g.get_vertices() - {v}}
    g.add_edges(*[tuple(e) for e in possible_edges if random() < p])
    return g


def hypercube_generation(dim):
    # generates a new graph with the structure of a dim-hypercube
    vertices = [i for i in range(2 ** dim)]
    edges = [(v, u,) for v in vertices for u in vertices if hamming_distance(v, u) == 1]
    g = Graph()
    g.add_vertices(*vertices)
    g.add_edges(*edges)
    return g


def ngon_generation(n: int):
    g = Graph()
    g.add_vertices(*[i for i in range(n)])
    g.add_edges(*[(i, (i+1) % n,) for i in range(n)])
    return g
