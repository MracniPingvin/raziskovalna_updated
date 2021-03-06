__author__ = 'FAMILY'
from tkinter import *

class GraphDraw(object):
    # class used for drawing an instance of class Graph
    def __init__(self, graph, size, sizex):

        self.graph = graph  # graph to be drawn
        self.size = size  # size in px
        self.sizex = sizex  # number of nodes in each row

        # square canvas
        self.canvas_width = self.size
        self.canvas_height = self.size

        self.node_map = self.generate_node_map()  # the coordinates of each node

        self.line_thickness = 5  # thickness of the connection lines
        self.circle_radius = 10  # radius of the node circles

        self.shape_queue = []  # list of instances of class Shape to be drawn

    def draw(self):
        # creates canvas and draws the elements on it
        master = Tk()
        self.canvas = Canvas(master, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()
        self.draw_node_map()
        for i in self.shape_queue:
            self.draw_shape(i)
        mainloop()

    def create_circle(self, x, y, r, **kwargs):
        return self.canvas.create_oval(x - r, y - r, x + r, y + r, **kwargs)

    def generate_node_map(self):
        # generates the list of coordinates of the nodes in the graph, depending on the type of the graph
        distance = self.size // (self.sizex + 1)
        node_map = []
        for j in range(self.sizex):
            for i in range(self.sizex):
                if self.graph.graph_type == "triangular" and j % 2 != 0:
                    node_map.append([1.5 *distance + i * distance, distance + j * distance])
                else:
                    node_map.append([distance + i * distance,distance + j * distance])
        return node_map

    def draw_node_map(self):
        # draws circles on the coordinates in node_map
        for i in self.node_map:
            self.create_circle(i[0], i[1], self.circle_radius, fill="cyan")

    def connect_nodes_triangular(self,edge,first=1,direction=None):
        # draws a segment of a shape in a triangular graph according to the layer the shape belongs to
        start_node = edge[0]
        end_node = edge[1]
        letter = edge[3]
        if self.node_map[end_node][0] == self.node_map[start_node][0]:
            orientation = 'y'
        elif self.node_map[end_node][1] == self.node_map[start_node][1]:
            orientation = 'x'
        else:
            orientation = 'd'

        offset = self.line_thickness
        soffset = int(offset * 0.70)
        text_offset = 15
        if first == 1:
            if direction == None:
                self.canvas.create_line(self.node_map[start_node][0] - offset,
                                        self.node_map[start_node][1] - offset,
                                        self.node_map[end_node][0] - offset,
                                        self.node_map[end_node][1] - offset,
                                        fill="#FF0000",width=5)

            elif direction == 0:
                self.canvas.create_line(self.node_map[start_node][0] + self.circle_radius,
                                        self.node_map[start_node][1] - offset,
                                        self.node_map[end_node][0] - offset,
                                        self.node_map[end_node][1] - offset,
                                        fill="#FF0000",width=5)
            elif direction == 1:
                self.canvas.create_line(self.node_map[start_node][0] - offset,
                                        self.node_map[start_node][1] + self.circle_radius,
                                        self.node_map[end_node][0] - offset,
                                        self.node_map[end_node][1] - offset,
                                        fill="#FF0000",width=5)
            elif direction == 2:
                self.canvas.create_line(self.node_map[start_node][0] - soffset,
                                        self.node_map[start_node][1] - soffset,
                                        self.node_map[end_node][0] - soffset,
                                        self.node_map[end_node][1] - soffset,
                                        fill="#FF0000",width=5)
            elif direction == 3:
                self.canvas.create_line(self.node_map[start_node][0] - self.circle_radius,
                                        self.node_map[start_node][1] - offset,
                                        self.node_map[end_node][0] - offset,
                                        self.node_map[end_node][1] - offset,
                                        fill="#FF0000",width=5)
            elif direction == 4:
                self.canvas.create_line(self.node_map[start_node][0] - offset,
                                        self.node_map[start_node][1] - self.circle_radius,
                                        self.node_map[end_node][0] - offset,
                                        self.node_map[end_node][1] - offset,
                                        fill="#FF0000",width=5)
            elif direction == 5:
                self.canvas.create_line(self.node_map[start_node][0] - soffset,
                                        self.node_map[start_node][1] - soffset,
                                        self.node_map[end_node][0] - soffset,
                                        self.node_map[end_node][1] - soffset,
                                        fill="#FF0000",width=5)
            if orientation == 'x':
                self.canvas.create_text((self.node_map[start_node][0] + self.node_map[end_node][0]) // 2,
                                        self.node_map[start_node][1] - text_offset,
                                        text=letter,fill="#FF0000")
            elif orientation == 'y':
                self.canvas.create_text(self.node_map[start_node][0] - text_offset,
                                         (self.node_map[start_node][1] + self.node_map[end_node][1]) // 2,
                                        text=letter,fill="#FF0000")
            elif orientation == 'd':
                self.canvas.create_text((self.node_map[start_node][0] + self.node_map[end_node][0]) // 2 - text_offset,
                                        (self.node_map[start_node][1] + self.node_map[end_node][1]) // 2 - text_offset,
                                        text=letter,fill="#FF0000")
        elif first == 3:
            if direction == None:
                self.canvas.create_line(self.node_map[start_node][0] + offset,
                                        self.node_map[start_node][1] + offset,
                                        self.node_map[end_node][0] + offset,
                                        self.node_map[end_node][1] + offset,
                                        fill="#00FF00",width=5)
            elif direction == 0:
                self.canvas.create_line(self.node_map[start_node][0] + self.circle_radius,
                                        self.node_map[start_node][1] + offset,
                                        self.node_map[end_node][0] + offset,
                                        self.node_map[end_node][1] + offset,
                                        fill="#00FF00",width=5)
            elif direction == 1:
                self.canvas.create_line(self.node_map[start_node][0] + offset,
                                        self.node_map[start_node][1] + self.circle_radius,
                                        self.node_map[end_node][0] + offset,
                                        self.node_map[end_node][1] + offset,
                                        fill="#00FF00",width=5)
            elif direction == 2:
                self.canvas.create_line(self.node_map[start_node][0] + soffset,
                                        self.node_map[start_node][1] + soffset,
                                        self.node_map[end_node][0] + soffset,
                                        self.node_map[end_node][1] + soffset,
                                        fill="#00FF00",width=5)
            elif direction == 3:
                self.canvas.create_line(self.node_map[start_node][0] - self.circle_radius,
                                        self.node_map[start_node][1] + offset,
                                        self.node_map[end_node][0] + offset,
                                        self.node_map[end_node][1] + offset,
                                        fill="#00FF00",width=5)
            elif direction == 4:
                self.canvas.create_line(self.node_map[start_node][0] + offset,
                                        self.node_map[start_node][1] - self.circle_radius,
                                        self.node_map[end_node][0] + offset,
                                        self.node_map[end_node][1] + offset,
                                        fill="#00FF00",width=5)
            elif direction == 5:
                self.canvas.create_line(self.node_map[start_node][0] + soffset,
                                        self.node_map[start_node][1] + soffset,
                                        self.node_map[end_node][0] + soffset,
                                        self.node_map[end_node][1] + soffset,
                                        fill="#00FF00",width=5)
            if orientation == 'x':
                self.canvas.create_text((self.node_map[start_node][0] + self.node_map[end_node][0]) // 2,
                                        self.node_map[start_node][1] + text_offset,
                                        text=letter,fill="#00FF00")
            elif orientation == 'y':
                self.canvas.create_text(self.node_map[start_node][0] + text_offset,
                                        (self.node_map[start_node][1] + self.node_map[end_node][1]) // 2,
                                        text=letter,fill="#00FF00")
            elif orientation == 'd':
                self.canvas.create_text((self.node_map[start_node][0] + self.node_map[end_node][0]) // 2 + text_offset,
                                        (self.node_map[start_node][1] + self.node_map[end_node][1]) // 2 + text_offset,
                                        text=letter,fill="#00FF00")
        elif first == 2:
            if direction == None:
                self.canvas.create_line(self.node_map[start_node][0],
                                        self.node_map[start_node][1],
                                        self.node_map[end_node][0],
                                        self.node_map[end_node][1],
                                        fill="#0000FF",width=5)
            elif direction == 0:
                self.canvas.create_line(self.node_map[start_node][0] + self.circle_radius,
                                        self.node_map[start_node][1],
                                        self.node_map[end_node][0],
                                        self.node_map[end_node][1],
                                        fill="#0000FF",width=5)
            elif direction == 1:
                self.canvas.create_line(self.node_map[start_node][0],
                                        self.node_map[start_node][1] + self.circle_radius,
                                        self.node_map[end_node][0],
                                        self.node_map[end_node][1],
                                        fill="#0000FF",width=5)
            elif direction == 2:
                self.canvas.create_line(self.node_map[start_node][0] - int(self.circle_radius*0.707),
                                        self.node_map[start_node][1] + int(self.circle_radius*0.707),
                                        self.node_map[end_node][0],
                                        self.node_map[end_node][1],
                                        fill="#0000FF",width=5)
            elif direction == 3:
                self.canvas.create_line(self.node_map[start_node][0] - self.circle_radius,
                                        self.node_map[start_node][1],
                                        self.node_map[end_node][0],
                                        self.node_map[end_node][1],
                                        fill="#0000FF",width=5)
            elif direction == 4:
                self.canvas.create_line(self.node_map[start_node][0],
                                        self.node_map[start_node][1] - self.circle_radius,
                                        self.node_map[end_node][0],
                                        self.node_map[end_node][1],
                                        fill="#0000FF",width=5)
            elif direction == 5:
                self.canvas.create_line(self.node_map[start_node][0] + int(self.circle_radius * 0.707),
                                        self.node_map[start_node][1] - int(self.circle_radius * 0.707),
                                        self.node_map[end_node][0],
                                        self.node_map[end_node][1],
                                        fill="#0000FF",width=5)
            if orientation == 'x':
                self.canvas.create_text((self.node_map[start_node][0] + self.node_map[end_node][0]) // 2 + 15,
                                        self.node_map[start_node][1] + text_offset,
                                        text=letter,fill="#0000FF")
            elif orientation == 'y':
                self.canvas.create_text(self.node_map[start_node][0] + text_offset,
                                        (self.node_map[start_node][1] + self.node_map[end_node][1]) // 2 + 15,
                                        text=letter,fill="#0000FF")
            elif orientation == 'd':
                self.canvas.create_text((self.node_map[start_node][0] + self.node_map[end_node][0]) // 2 + text_offset,
                                        (self.node_map[start_node][1] + self.node_map[end_node][1]) // 2 + text_offset + 15,
                                        text=letter,fill="#0000FF")

    def connect_nodes_squared(self, edge, first=1, direction=None):
        # draws a segment of a shape in a squared graph according to the layer the shape belongs to
        start_node = edge[0]
        end_node = edge[1]
        letter = edge[3]
        if self.node_map[end_node][0] == self.node_map[start_node][0]:
            orientation = 'y'
        else:
            orientation = 'x'
        offset = self.line_thickness
        text_offset = 15
        if first == 1:
            if direction == None:
                self.canvas.create_line(self.node_map[start_node][0] - offset,
                                        self.node_map[start_node][1] - offset,
                                        self.node_map[end_node][0] - offset,
                                        self.node_map[end_node][1] - offset,
                                        fill="#FF0000", width=5)

            elif direction == 0:
                self.canvas.create_line(self.node_map[start_node][0] + self.circle_radius,
                                        self.node_map[start_node][1] - offset,
                                        self.node_map[end_node][0] - offset,
                                        self.node_map[end_node][1] - offset,
                                        fill="#FF0000", width=5)
            elif direction == 1:
                self.canvas.create_line(self.node_map[start_node][0] - offset,
                                        self.node_map[start_node][1] + self.circle_radius,
                                        self.node_map[end_node][0] - offset,
                                        self.node_map[end_node][1] - offset,
                                        fill="#FF0000", width=5)
            elif direction == 2:
                self.canvas.create_line(self.node_map[start_node][0] - self.circle_radius,
                                        self.node_map[start_node][1] - offset,
                                        self.node_map[end_node][0] - offset,
                                        self.node_map[end_node][1] - offset,
                                        fill="#FF0000", width=5)
            elif direction == 3:
                self.canvas.create_line(self.node_map[start_node][0] - offset,
                                        self.node_map[start_node][1] - self.circle_radius,
                                        self.node_map[end_node][0] - offset,
                                        self.node_map[end_node][1] - offset,
                                        fill="#FF0000", width=5)
            if orientation == 'x':
                self.canvas.create_text((self.node_map[start_node][0] + self.node_map[end_node][0]) // 2,
                                        self.node_map[start_node][1] - text_offset,
                                        text=letter, fill="#FF0000")
            else:
                self.canvas.create_text(self.node_map[start_node][0] - text_offset,
                                        (self.node_map[start_node][1] + self.node_map[end_node][1]) // 2,
                                        text=letter, fill="#FF0000")
        elif first == 2:
            if direction == None:
                self.canvas.create_line(self.node_map[start_node][0] + offset,
                                        self.node_map[start_node][1] + offset,
                                        self.node_map[end_node][0] + offset,
                                        self.node_map[end_node][1] + offset,
                                        fill="#00FF00", width=5)
            elif direction == 0:
                self.canvas.create_line(self.node_map[start_node][0] + self.circle_radius,
                                        self.node_map[start_node][1] + offset,
                                        self.node_map[end_node][0] + offset,
                                        self.node_map[end_node][1] + offset,
                                        fill="#00FF00", width=5)
            elif direction == 1:
                self.canvas.create_line(self.node_map[start_node][0] + offset,
                                        self.node_map[start_node][1] + self.circle_radius,
                                        self.node_map[end_node][0] + offset,
                                        self.node_map[end_node][1] + offset,
                                        fill="#00FF00", width=5)
            elif direction == 2:
                self.canvas.create_line(self.node_map[start_node][0] - self.circle_radius,
                                        self.node_map[start_node][1] + offset,
                                        self.node_map[end_node][0] + offset,
                                        self.node_map[end_node][1] + offset,
                                        fill="#00FF00", width=5)
            elif direction == 3:
                self.canvas.create_line(self.node_map[start_node][0] + offset,
                                        self.node_map[start_node][1] - self.circle_radius,
                                        self.node_map[end_node][0] + offset,
                                        self.node_map[end_node][1] + offset,
                                        fill="#00FF00", width=5)
            if orientation == 'x':
                self.canvas.create_text((self.node_map[start_node][0] + self.node_map[end_node][0]) // 2,
                                        self.node_map[start_node][1] + text_offset,
                                        text=letter, fill="#00FF00")
            else:
                self.canvas.create_text(self.node_map[start_node][0] + text_offset,
                                        (self.node_map[start_node][1] + self.node_map[end_node][1]) // 2,
                                        text=letter, fill="#00FF00")
        elif first == 3:
            if direction == None:
                self.canvas.create_line(self.node_map[start_node][0],
                                        self.node_map[start_node][1],
                                        self.node_map[end_node][0],
                                        self.node_map[end_node][1],
                                        fill="#0000FF", width=5)
            elif direction == 0:
                self.canvas.create_line(self.node_map[start_node][0] + self.circle_radius,
                                        self.node_map[start_node][1],
                                        self.node_map[end_node][0],
                                        self.node_map[end_node][1],
                                        fill="#0000FF", width=5)
            elif direction == 1:
                self.canvas.create_line(self.node_map[start_node][0],
                                        self.node_map[start_node][1] + self.circle_radius,
                                        self.node_map[end_node][0],
                                        self.node_map[end_node][1],
                                        fill="#0000FF", width=5)
            elif direction == 2:
                self.canvas.create_line(self.node_map[start_node][0] - self.circle_radius,
                                        self.node_map[start_node][1],
                                        self.node_map[end_node][0],
                                        self.node_map[end_node][1],
                                        fill="#0000FF", width=5)
            elif direction == 3:
                self.canvas.create_line(self.node_map[start_node][0],
                                        self.node_map[start_node][1] - self.circle_radius,
                                        self.node_map[end_node][0],
                                        self.node_map[end_node][1],
                                        fill="#0000FF", width=5)
            if orientation == 'x':
                self.canvas.create_text((self.node_map[start_node][0] + self.node_map[end_node][0]) // 2 + 15,
                                        self.node_map[start_node][1] + text_offset,
                                        text=letter, fill="#0000FF")
            else:
                self.canvas.create_text(self.node_map[start_node][0] + text_offset,
                                        (self.node_map[start_node][1] + self.node_map[end_node][1]) // 2 + 15,
                                        text=letter, fill="#0000FF")

    def draw_shape(self, shape):
        # draws all the segments of a shape
        count = 0
        first = shape.first

        for i in shape.segment_list:
            if count == 0:
                if self.graph.graph_type == "triangular":
                    self.connect_nodes_triangular(i, first, i[2])
                elif self.graph.graph_type == "squared":
                    self.connect_nodes_squared(i, first, i[2])
            else:
                if self.graph.graph_type == "triangular":
                    self.connect_nodes_triangular(i, first)
                elif self.graph.graph_type == "squared":
                    self.connect_nodes_squared(i, first)
            count += 1
