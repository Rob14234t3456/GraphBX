from random import random


class Graph:
    def __init__(self):
        self._graph = dict()

    def add_vertices(self, *args):
        for v in args:
            self._graph[v] = set()

    def add_edge(self, v1, v2):
        self._graph[v1].add(v2)
        self._graph[v2].add(v1)

    def add_edges(self, *args):
        [self.add_edge(e[0], e[1]) for e in args]

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


def erdos_renyi_model_generation(g: Graph, p: float):
    # enumerate all possible edges of a graph using a method similar to the get_edges function
    # this is not most efficient, but it is easy

    possible_edges = {frozenset({v, u}) for v in g.get_vertices() for u in g.get_vertices() - {v}}
    g.add_edges(*[tuple(e) for e in possible_edges if random() < p])
