import http.server
import socketserver
import XMLParse
import Graphs
import GraphsRender
import json

PORT = 8000


class Handler(http.server.SimpleHTTPRequestHandler):
    @staticmethod
    def serve_request_test():
        print('test complete')

    def serve_request_random_graph(self, fields):
        # generates a random graph and stores it to the given path

        n = int(fields['n'])
        p = float(fields['p'])

        graph = Graphs.erdos_renyi_model_generation(n, p)
        coords = GraphsRender.generate_circle_coordinates(graph, 1000, 1000, 0.8)
        XMLParse.parse_graph_coords(graph, coords, self.path[1:])

        print('random graph generated with parameters n: {}, p:{} and stored to {}'.format(n, p, self.path))

    def serve_request_nearest_xy_vertex(self, fields):
        # finds the nearest xy vertex from the coordinate graph stored as XML at the given path
        # responds with vertex name
        x = float(fields['x'])
        y = float(fields['y'])
        graph = XMLParse.parse_xml_graph(self.path[1:] + fields['graph_path'])
        coords = XMLParse.parse_xml_graph_coordinates(self.path[1:] + fields['graph_path'])
        v = GraphsRender.nearest_vertex_xy(graph, coords, x, y)

        # send response
        self.send_response(200)
        self.send_header("Content-type", "text")
        self.end_headers()
        self.wfile.write(str(v).encode('utf-8'))

    def serve_request_shortest_path(self, fields):
        # finds the shortest path from fields[v1] to fields[v2] in parsed graph at graph_path
        # responds with a JSON list of vertices in path order
        v1 = eval(fields['v1'])
        v2 = eval(fields['v2'])
        graph = XMLParse.parse_xml_graph(self.path[1:] + fields['graph_path'])

        # find path and parse
        sp = graph.shortest_path(v1, v2)
        sp = [repr(v) for v in sp]
        sp = json.dumps(sp)

        # send response
        self.send_response(200)
        self.send_header("Content-type", "text")
        self.end_headers()
        self.wfile.write(sp.encode('utf-8'))

    def do_POST(self):
        length = int(self.headers.get('content-length'))
        field_data = self.rfile.read(length)
        fields = json.loads(field_data)
        request_type = fields['request_type']

        #try:
        #    if request_type == 'test':
        #        self.serve_request_test()
        #    elif request_type == 'random_graph_generation':
        #        self.serve_request_random_graph(fields)
        #    elif request_type == 'nearest_xy_vertex':
        #        self.serve_request_nearest_xy_vertex(fields)
        #    elif request_type == 'shortest_path':
        #        self.serve_request_shortest_path(fields)
        #    else:
        #        raise BaseException('No such request type as "{}" supported'.format(fields['request_type']))
#
        #except BaseException:
        #    self.send_error(400)

        if request_type == 'test':
            self.serve_request_test()
        elif request_type == 'random_graph_generation':
            self.serve_request_random_graph(fields)
        elif request_type == 'nearest_xy_vertex':
            self.serve_request_nearest_xy_vertex(fields)
        elif request_type == 'shortest_path':
            self.serve_request_shortest_path(fields)
        else:
            raise BaseException('No such request type as "{}" supported'.format(fields['request_type']))



with socketserver.TCPServer(("localhost", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
