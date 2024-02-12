from math import pi
from xml.dom.minidom import Entity

from tools.target import Target
from tools.vector import Vector2

from model.behaviours.pendulum import Pendulum as PhysicsPendulumModel
from view.behaviours.pendulum import Pendulum as PhysicsPendulumView


class PhysicsPendulum:
    def __init__(self, canvas, params):
        self.id = None
        self.canvas = canvas
        self.params = params
        self.end = Vector2(0, 0)
        self.axis = Vector2(200, 200)
        self.name_coords = Vector2(-20, -20)
        self.name = "Маятник"
        self.position = Vector2(0, 0)
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)
        self.start_tick = 0
        self.start_angle = pi / 4
        self.previous_angle = pi / 4
        self.angle = pi / 4
        self.full_angle = 0
        self.custom_inertia_moment = 1
        self.custom_mass_center_remoteness = 0.5
        self.angle_acceleration = 0
        self.angle_velocity = 0
        self.previous_angle_velocity = self.angle_velocity
        self.size = 1
        self.type = "thin_walled_rod"
        self.mass = 10
        self.mass_center_remoteness = 0.5
        self.counterweight_size = 0
        self.inertia_moment = (1 / 12) * (self.size + self.counterweight_size) ** 2 * self.mass
        self.model = PhysicsPendulumModel(self)
        self.view = PhysicsPendulumView(self)

        self.targets = {"a": Target(self.angle), "av": Target(self.angle_velocity), "aa": Target(self.angle_acceleration), "fa": Target(self.full_angle)}

    def restart(self):
        self.angle = self.start_angle
        self.angle_acceleration = 0
        self.angle_velocity = 0
        self.full_angle = 0
        self.start_tick = self.params["model_tick"]

    def delete(self):
        self.params["model"].entities.pop(self.id)
        self.params["view"].entities.pop(self.id)
        self.view.delete()
