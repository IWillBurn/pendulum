from math import sin, sqrt, cos, pi

from tools.steiner import steiner
from tools.vector import Vector2


class PhysicsPendulum:
    def __init__(self, main):
        self.main = main

    def step(self):
        force = Vector2(0, 0)

        part = self.main.mass_center_remoteness * (
                self.main.size + self.main.counterweight_size) - self.main.counterweight_size
        center_len_x = cos(self.main.angle + pi / 2) * part + self.main.axis.x
        center_len_y = sin(self.main.angle + pi / 2) * part + self.main.axis.y

        remoteness = sqrt((self.main.axis.x - center_len_x)**2 + (self.main.axis.y - center_len_y)**2)
        inertia_moment = steiner(self.main.inertia_moment, self.main.mass,
                                 remoteness * (self.main.size + self.main.counterweight_size))
        self.main.angle_acceleration = - (self.main.params["g"] * self.main.mass - force.y) * remoteness * sin(self.main.angle) / inertia_moment
        self.main.angle_velocity += self.main.angle_acceleration * self.main.params["dt"]
        self.main.angle += self.main.angle_velocity * self.main.params["dt"]


class MathPendulum:
    def __init__(self, main):
        self.main = main

    def step(self):
        self.main.velocity.add(self.main.acceleration.multiply_to_scalar_value(self.main.params["dt"]))
        self.main.position.add(self.main.velocity.multiply_to_scalar_value(self.main.params["dt"]))
