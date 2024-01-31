from math import pi
from xml.dom.minidom import Entity

from tools.vector import Vector2

from model.behaviours.pendulum import PhysicsPendulum as PhysicsPendulumModel
from view.behaviours.pendulum import PhysicsPendulum as PhysicsPendulumView


class PhysicsPendulum:
    def __init__(self, canvas, params):
        self.canvas = canvas
        self.params = params
        self.position = Vector2(0, 0)
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)
        self.axis = Vector2(100, 100)
        self.angle = pi / 4
        self.angle_acceleration = 0
        self.angle_velocity = 0
        self.size = 1
        self.mass = 1
        self.mass_center_remoteness = 0.5
        self.counterweight_size = 0.1
        self.inertia_moment = (1 / 12) * (self.size + self.counterweight_size) ** 2 * self.mass
        self.model = PhysicsPendulumModel(self)
        self.view = PhysicsPendulumView(self)


class MathPendulum:
    def __init__(self, canvas, params):
        self.canvas = canvas
        self.params = params
        self.position = Vector2(0, 400)
        self.velocity = Vector2(10, -10)
        self.acceleration = Vector2(0, 10)
        self.model = PhysicsPendulumModel(self)
        self.view = PhysicsPendulumView(self)
