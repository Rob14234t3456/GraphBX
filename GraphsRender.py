from Graphs import *
import tkinter as tk
from math import cos, sin, pi
from random import random
from MathOperations import xy_distance


font = ("Times", 16)


class Canvas(tk.Canvas):
    def __init__(self, w, h, **kw):
        self.top = tk.Tk()
        super().__init__(self.top, height=h, width=w, **kw)

    def create_dot(self, x, y, r, colour="black"):
        self.create_oval(x - r, y - r, x + r, y + r, fill=colour)

    def begin_mainloop(self):
        self.pack()
        self.top.mainloop()


def render_graph_circle(canvas: Canvas, g: Graph, h: float, w: float, padding: float, label_padding: float):
    coords = generate_circle_coordinates(g, h, w, padding)
    render_graph_coordinate(canvas, g, coords, label_padding)


def generate_circle_coordinates(g: Graph, h: float, w: float, padding: float):
    vertices = list(g.vertices)
    n = len(vertices)
    coords = dict()

    # generate vertex coordinates in a circle
    for i in range(0, n):
        xc = (w/2) * (1 + (padding * cos(i*2*pi/n)))
        yc = (h/2) * (1 + (padding * sin(i*2*pi/n)))
        coords[vertices[i]] = (xc, yc,)

    return coords


def render_graph_random(canvas: Canvas, g: Graph, h: float, w: float, label_padding: float):
    coords = generate_random_coordinates(g, h, w)
    render_graph_coordinate(canvas, g, coords, label_padding)


def generate_random_coordinates(g: Graph, h: float, w: float):
    coords = dict()

    # generate random coordinate set
    for v in g.vertices:
        coords[v] = (random() * w, random() * h,)

    return coords


def render_graph_coordinate(canvas: Canvas, g: Graph, coords: dict, label_padding: float):
    # coords should be a dict mapping g's vertices to 2-d coordinates
    # draw vertices
    for v in g.vertices:
        xc = coords[v][0]
        yc = coords[v][1]
        canvas.create_dot(xc, yc, 10)
        canvas.create_text(xc, yc - label_padding, text=v, font=font)

    for e in g.edges:
        canvas.create_line(coords[e[0]], coords[e[1]])


def render_graph_coordinate_style(canvas: Canvas, g: Graph, h: float, w: float, coords: dict, label_padding: float,
                                  colour, line_thickness, dot_size):
    # coords should be a dict mapping g's vertices to 2-d coordinates
    # draw vertices
    for v in g.vertices:
        xc = coords[v][0]
        yc = coords[v][1]
        canvas.create_dot(xc, yc, dot_size, colour=colour)
        canvas.create_text(xc, yc - label_padding, text=v, font=font)

    for e in g.edges:
        canvas.create_line(coords[e[0]], coords[e[1]], fill=colour, width=line_thickness)


def nearest_vertex_xy(graph: BasicGraph, coords: dict, x: float, y: float):
    listed_vertices = list(graph.vertices)
    distances = [xy_distance(x, y, coords[v][0], coords[v][1]) for v in listed_vertices]
    return listed_vertices[distances.index(min(distances))]
