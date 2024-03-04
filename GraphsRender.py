from Graphs import *
import tkinter as tk
from math import cos, sin, pi


font = ("Times", 16)


class Canvas2(tk.Canvas):
    def create_dot(self, x, y, r):
        self.create_oval(x - r, y - r, x + r, y + r, fill="black")


def render_graph(g: Graph, h: float, w: float, padding: float, padding2: float):
    top = tk.Tk()
    canvas = Canvas2(top, height=h, width=w)

    vertices = list(g.get_vertices())
    l = len(vertices)
    coords = dict()

    # draw vertices
    for i in range(0, l):
        xc = (w/2) * (1 + (padding * cos(i*2*pi/l)))
        yc = (h/2) * (1 + (padding * sin(i*2*pi/l)))
        xc2 = (w/2) * (1 + (padding2 * cos(i*2*pi/l)))
        yc2 = (h/2) * (1 + (padding2 * sin(i*2*pi/l)))

        coords[vertices[i]] = (xc, yc,)
        canvas.create_dot(xc, yc, 10)
        canvas.create_text(xc2, yc2, text=vertices[i], font=font)

    # draw edges
    # for u in vertices:
    #     for v in g.neighbourhood(u):
    #         canvas.create_line(coords[u], coords[v])

    for e in g.get_edges():
        canvas.create_line(coords[e[0]], coords[e[1]])

    canvas.pack()
    top.mainloop()
