from math import sin, sqrt, cos, pi

from tools.steiner import steiner
from tools.vector import Vector2


class Pendulum:
    def __init__(self, main):
        self.main = main
        self.steps = {
            "math": self.step_math,
            "thin_walled_rod": self.step_thin_walled_rod,
            "custom": self.step_custom,
        }

    def step_math(self):
        o = self.main.params["g"] / self.main.size * (1 - self.main.counterweight_size)
        self.main.angle = self.main.start_angle * cos((self.main.params["model_tick"] - self.main.start_tick) * self.main.params["dt"] * o)
        self.main.angle_velocity = (self.main.angle - self.main.previous_angle) / self.main.params["dt"]
        self.main.angle_acceleration = (self.main.angle_velocity - self.main.previous_angle_velocity) / self.main.params["dt"]
        self.main.full_angle += abs(self.main.angle - self.main.previous_angle)
        self.main.previous_angle = self.main.angle
        self.main.previous_angle_velocity = self.main.angle_velocity

    def step_thin_walled_rod(self):
        force = Vector2(0, 0)

        part = abs(self.main.mass_center_remoteness - self.main.counterweight_size) * self.main.size
        center_len_x = cos(self.main.angle + pi / 2) * part + self.main.axis.x
        center_len_y = sin(self.main.angle + pi / 2) * part + self.main.axis.y

        self.main.remoteness = sqrt((self.main.axis.x - center_len_x) ** 2 + (self.main.axis.y - center_len_y) ** 2)
        self.main.inertia_moment = steiner((1 / 12) * ((self.main.size) ** 2) * self.main.mass, self.main.mass, self.main.remoteness)
        self.main.angle_acceleration = - (self.main.params["g"] * self.main.mass - force.y) * self.main.remoteness * sin(self.main.angle) / self.main.inertia_moment
        self.main.angle_velocity += self.main.angle_acceleration * self.main.params["dt"]
        self.main.angle += self.main.angle_velocity * self.main.params["dt"]
        self.main.full_angle += abs(self.main.angle_velocity * self.main.params["dt"])


    def step_custom(self):
        force = Vector2(0, 0)
        self.main.angle_acceleration = - (self.main.params["g"] * self.main.mass - force.y) * self.main.custom_mass_center_remoteness * sin(self.main.angle) / self.main.custom_inertia_moment
        self.main.angle_velocity += self.main.angle_acceleration * self.main.params["dt"]
        self.main.angle += self.main.angle_velocity * self.main.params["dt"]
        self.main.mass_center_remoteness = self.main.custom_mass_center_remoteness
        self.main.full_angle += abs(self.main.angle_velocity * self.main.params["dt"])

    def update_targets(self):
        self.main.targets["a"].value = self.main.angle
        self.main.targets["av"].value = self.main.angle_velocity
        self.main.targets["aa"].value = self.main.angle_acceleration
        self.main.targets["fa"].value = self.main.full_angle

    def step(self):
        self.steps[self.main.type]()
        self.normalize_angle()
        self.update_targets()

    def normalize_angle(self):
        while self.main.angle < -pi:
            self.main.angle += 2 * pi

        while self.main.angle >= pi:
            self.main.angle -= 2 * pi