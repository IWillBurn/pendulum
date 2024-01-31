from tools.vector import Vector2
from model.behaviours.point import Point2D as Point2DModel
from view.behaviours.point import Point2D as Point2DView


class Point2D:
    def __init__(self, canvas, params):
        self.canvas = canvas
        self.params = params
        self.position = Vector2(0, 400)
        self.velocity = Vector2(10, -10)
        self.acceleration = Vector2(0, 10)
        self.model = Point2DModel(self)
        self.view = Point2DView(self)
