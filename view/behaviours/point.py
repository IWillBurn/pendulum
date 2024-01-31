from tools.vector import Vector2
import tkinter as tk


class Point2D:
    def __init__(self, main):
        self.main = main
        self.object = None

    def initialize(self):
        self.object = self.main.canvas.create_oval(1, 1, 8, 8, fill="red", outline="white")

    def draw(self):
        delta_x = self.main.position.x - self.main.canvas.coords(self.object)[0]
        delta_y = self.main.position.y - self.main.canvas.coords(self.object)[1]
        self.main.canvas.move(self.object, delta_x, delta_y)
