from math import sin, cos, pi, sqrt

from tools.vector import Vector2
import tkinter as tk


class PhysicsPendulum:
    def __init__(self, main):
        self.name = None
        self.main = main
        self.object = None
        self.counterweight = None
        self.axis = None
        self.center = None
        self.end = None
        self.is_dragging = [False, False, False]

    def pick_axis(self, event):
        self.is_dragging[0] = True
        self.main.params["selected"][1] = self.main
        self.main.params["selected"][0] = True


    def drop_axis(self, event):
        self.is_dragging[0] = False

    def drag_axis(self, event):
        if self.is_dragging[0]:
            self.main.axis = Vector2(event.x, event.y)

    def pick_end(self, event):
        self.is_dragging[1] = True
        self.main.params["selected"][1] = self.main
        self.main.params["selected"][0] = True

    def drop_end(self, event):
        self.is_dragging[1] = False

    def drag_end(self, event):
        if self.is_dragging[1]:
            self.main.params["selected"][0] = True
            size = self.main.size # + self.main.counterweight_size
            main_size = sqrt((event.x - self.main.axis.x) ** 2 + (event.y - self.main.axis.y) ** 2) / self.main.params[
                "scale"]
            if size - main_size > 0:
                self.main.counterweight_size = (size - main_size) / size

    def select(self, event):
        self.main.params["selected"][1] = self.main
        self.main.params["selected"][0] = True

    '''
    def pick_center(self, event):
        self.is_dragging[2] = True

    def drop_center(self, event):
        self.is_dragging[2] = False

    def drag_center(self, event):
        if self.is_dragging[2]:
            center_len = self.main.counterweight_size + sqrt((event.x - self.main.axis.x)**2 + (event.y - self.main.axis.y)**2)
            if center_len < self.main.size + self.main.counterweight_size:
                self.main.mass_center_remoteness = center_len / (self.main.size + self.main.counterweight_size)
    '''

    def initialize(self):

        self.name = self.main.canvas.create_text(self.main.axis.x + self.main.name_coords.x, self.main.axis.y + self.main.name_coords.y, text=self.main.name, fill="black")

        self.object = self.main.canvas.create_line(0, 0, 10, 10, width=5, fill="gray")
        self.counterweight = self.main.canvas.create_line(0, 0, 5, 5, width=5, fill="black")
        self.axis = self.main.canvas.create_oval(1, 1, 15, 15, fill="black", outline="black")
        self.end = self.main.canvas.create_oval(1, 1, 15, 15, fill="red", outline="red")
        self.center = self.main.canvas.create_oval(1, 1, 8, 8, fill="blue", outline="blue")

        self.main.canvas.tag_bind(self.axis, '<ButtonPress-1>', self.pick_axis)
        self.main.canvas.tag_bind(self.axis, '<ButtonRelease-1>', self.drop_axis)
        self.main.canvas.tag_bind(self.axis, '<B1-Motion>', self.drag_axis)

        self.main.canvas.tag_bind(self.end, '<ButtonPress-1>', self.pick_end)
        self.main.canvas.tag_bind(self.end, '<ButtonRelease-1>', self.drop_end)
        self.main.canvas.tag_bind(self.end, '<B1-Motion>', self.drag_end)

        self.main.canvas.tag_bind(self.object, '<ButtonPress-1>', self.select)
        self.main.canvas.tag_bind(self.counterweight, '<ButtonPress-1>', self.select)

        '''
        self.main.canvas.tag_bind(self.center, '<ButtonPress-1>', self.pick_center)
        self.main.canvas.tag_bind(self.center, '<ButtonRelease-1>', self.drop_center)
        self.main.canvas.tag_bind(self.center, '<B1-Motion>', self.drag_center)
        '''

    def draw(self):



        len_x = cos(self.main.angle + pi / 2) * self.main.size * (1 - self.main.counterweight_size) * self.main.params["scale"]
        len_y = sin(self.main.angle + pi / 2) * self.main.size * (1 - self.main.counterweight_size) * self.main.params["scale"]

        counterweight_x = cos(self.main.angle + pi / 2) * self.main.counterweight_size * self.main.size * self.main.params["scale"]
        counterweight_y = sin(self.main.angle + pi / 2) * self.main.counterweight_size * self.main.size * self.main.params["scale"]

        self.main.canvas.coords(self.object, self.main.axis.x, self.main.axis.y, self.main.axis.x + len_x,
                                self.main.axis.y + len_y)
        self.main.canvas.coords(self.counterweight, self.main.axis.x, self.main.axis.y,
                                self.main.axis.x - counterweight_x, self.main.axis.y - counterweight_y)

        end_coords = self.main.canvas.coords(self.end)
        delta_x = self.main.axis.x + len_x - (end_coords[0] + end_coords[2]) / 2
        delta_y = self.main.axis.y + len_y - (end_coords[1] + end_coords[3]) / 2
        self.main.canvas.move(self.end, delta_x, delta_y)
        end_coords = self.main.canvas.coords(self.end)
        self.main.end.x = (end_coords[0] + end_coords[2]) / 2
        self.main.end.y = (end_coords[1] + end_coords[3]) / 2

        axis_coords = self.main.canvas.coords(self.axis)
        delta_x = self.main.axis.x - (axis_coords[0] + axis_coords[2]) / 2
        delta_y = self.main.axis.y - (axis_coords[1] + axis_coords[3]) / 2
        self.main.canvas.move(self.axis, delta_x, delta_y)

        part = self.main.mass_center_remoteness * self.main.size
        center_len_x = cos(self.main.angle + pi / 2) * part * self.main.params["scale"] + self.main.axis.x - counterweight_x
        center_len_y = sin(self.main.angle + pi / 2) * part * self.main.params["scale"] + self.main.axis.y - counterweight_y
        center_coords = self.main.canvas.coords(self.center)
        delta_x = center_len_x - (center_coords[0] + center_coords[2]) / 2
        delta_y = center_len_y - (center_coords[1] + center_coords[3]) / 2
        self.main.canvas.move(self.center, delta_x, delta_y)

        name_coords = self.main.canvas.coords(self.name)
        delta_x = self.main.axis.x + self.main.name_coords.x - name_coords[0]
        delta_y = self.main.axis.y + self.main.name_coords.y - name_coords[1]
        self.main.canvas.move(self.name, delta_x, delta_y)
        self.main.canvas.itemconfig(self.name, text=self.main.name)


class MathPendulum:
    def __init__(self, main):
        self.main = main
        self.object = None

    def initialize(self):
        self.object = self.main.canvas.create_oval(1, 1, 8, 8, fill="red", outline="white")

    def draw(self):
        delta_x = self.main.position.x - self.main.canvas.coords(self.object)[0]
        delta_y = self.main.position.y - self.main.canvas.coords(self.object)[1]
        self.main.canvas.move(self.object, delta_x, delta_y)
