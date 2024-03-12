import http.server
import socketserver
import XMLParse
import Graphs
import GraphsRender

PORT = 8000


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_RANDGRAPH(self):
        # serve a RANDGRAPH request
        # kinda janky, but uses the path attribute of an Http request to get n and m
        # generates a graph and stores to data.xml, which will need to be separately fetched
        # passed url should be of format "/n;p" with the / since otherwise the request
        # will add the relative domain url

        # first remove the / from the string
        print(self.path)
        data = self.path[1:]
        n, p = [i for i in data.split(";")]

        n = int(n)
        p = float(p)
        graph = Graphs.erdos_renyi_model_generation(n, p)
        coords = GraphsRender.generate_circle_coordinates(graph, 1000, 1000, 0.8)
        XMLParse.parse_graph_coords(graph, coords, "data.xml")


with socketserver.TCPServer(("localhost", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
