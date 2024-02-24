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
        self.start_angle = 0.1
        self.previous_angle = self.start_angle
        self.angle = self.start_angle
        self.full_angle = 0
        self.angle_acceleration = 0
        self.angle_velocity = 0
        self.previous_angle_velocity = self.angle_velocity
        self.size = 1
        self.type = "real"
        self.mass = 1
        self.mass_center_remoteness = 1
        self.gamma = 0
        self.counterweight_size = 0
        self.inertia_moment = 1
        self.model = PhysicsPendulumModel(self)
        self.view = PhysicsPendulumView(self)
        self.inertia_moment_formula = self.inertia_moment
        self.stop = False
        self.targets = {"a": Target(self.angle),
                        "r": Target(self.size),
                        "m": Target(self.mass),
                        "av": Target(self.angle_velocity),
                        "aa": Target(self.angle_acceleration),
                        "fa": Target(self.full_angle),
                        "rp": Target(self.counterweight_size),
                        "im": Target(self.inertia_moment),
                        "rmp": Target(self.mass_center_remoteness)}

    def update_targets(self):
        self.targets["a"].value = self.angle
        self.targets["r"].value = self.size
        self.targets["m"].value = self.mass
        self.targets["av"].value = self.angle_velocity
        self.targets["aa"].value = self.angle_acceleration
        self.targets["fa"].value = self.full_angle
        self.targets["rp"].value = self.counterweight_size
        self.targets["im"].value = self.inertia_moment
        self.targets["rmp"].value = self.mass_center_remoteness

    def restart(self):
        self.angle = self.start_angle
        self.angle_acceleration = 0
        self.angle_velocity = 0
        self.full_angle = 0
        self.previous_angle = self.angle
        self.previous_angle_velocity = 0
        self.start_tick = self.params["model_tick"]

    def delete(self):
        self.params["model"].entities.pop(self.id)
        self.params["view"].entities.pop(self.id)
        self.view.delete()
