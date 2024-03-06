from Graphs import *
import tkinter as tk
from math import cos, sin, pi
from random import random


font = ("Times", 16)


class Canvas(tk.Canvas):
    def __init__(self, w, h, **kw):
        self.top = tk.Tk()
        super().__init__(self.top, height=h, width=w, **kw)

    def create_dot(self, x, y, r, colour="black"):
        self.create_oval(x - r, y - r, x + r, y + r, fill=colour)


def render_graph_circle(g: Graph, h: float, w: float, padding: float, label_padding: float):
    vertices = list(g.get_vertices())
    n = len(vertices)
    coords = dict()

    # generate vertex coordinates in a circle
    for i in range(0, n):
        xc = (w/2) * (1 + (padding * cos(i*2*pi/n)))
        yc = (h/2) * (1 + (padding * sin(i*2*pi/n)))
        coords[vertices[i]] = (xc, yc,)

    render_graph_coordinate(g, h, w, coords, label_padding)


def generate_circle_coordinates(g: Graph, h: float, w: float, padding: float):
    vertices = list(g.get_vertices())
    n = len(vertices)
    coords = dict()

    # generate vertex coordinates in a circle
    for i in range(0, n):
        xc = (w/2) * (1 + (padding * cos(i*2*pi/n)))
        yc = (h/2) * (1 + (padding * sin(i*2*pi/n)))
        coords[vertices[i]] = (xc, yc,)

    return coords


def render_graph_random(g: Graph, h: float, w: float, label_padding: float):
    coords = dict()

    # generate random coordinate set
    for v in g.get_vertices():
        coords[v] = (random() * w, random() * h,)

    render_graph_coordinate(g, h, w, coords, label_padding)


def generate_random_coordinates(g: Graph, h: float, w: float):
    coords = dict()

    # generate random coordinate set
    for v in g.get_vertices():
        coords[v] = (random() * w, random() * h,)

    return coords


def render_graph_coordinate(canvas: Canvas, g: Graph, h: float, w: float, coords: dict, label_padding: float):
    # coords should be a dict mapping g's vertices to 2-d coordinates
    # draw vertices
    for v in g.get_vertices():
        xc = coords[v][0]
        yc = coords[v][1]
        canvas.create_dot(xc, yc, 10)
        canvas.create_text(xc, yc - label_padding, text=v, font=font)

    for e in g.get_edges():
        canvas.create_line(coords[e[0]], coords[e[1]])


def render_graph_coordinate_style(canvas: Canvas, g: Graph, h: float, w: float, coords: dict, label_padding: float,
                                  colour, line_thickness, dot_size):
    # coords should be a dict mapping g's vertices to 2-d coordinates
    # draw vertices
    for v in g.get_vertices():
        xc = coords[v][0]
        yc = coords[v][1]
        canvas.create_dot(xc, yc, dot_size, colour=colour)
        canvas.create_text(xc, yc - label_padding, text=v, font=font)

    for e in g.get_edges():
        canvas.create_line(coords[e[0]], coords[e[1]], fill=colour, width=line_thickness)


def begin_mainloop(canvas: Canvas):
    canvas.pack()
    canvas.top.mainloop()
