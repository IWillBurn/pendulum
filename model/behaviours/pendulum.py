from math import sin, sqrt, cos, pi

from tools.steiner import steiner
from tools.vector import Vector2


class Pendulum:
    def __init__(self, main):
        self.main = main
        self.steps = {
            "real": self.step_real,
            "theory": self.step_theory,
        }

    def step_real(self):
        o2 = self.main.params["g"] * self.main.mass * self.main.mass_center_remoteness * self.main.size / self.main.inertia_moment
        self.main.angle_acceleration = - o2 * sin(self.main.angle)
        self.main.angle_velocity += self.main.angle_acceleration * self.main.params["dt"]
        self.main.angle += self.main.angle_velocity * self.main.params["dt"]
        self.main.full_angle += abs(self.main.angle_velocity * self.main.params["dt"])

    def step_theory(self):
        o2 = self.main.params["g"] * self.main.mass * self.main.mass_center_remoteness * self.main.size / self.main.inertia_moment
        self.main.angle = self.main.start_angle * cos(sqrt(o2) * (self.main.params["model_tick"] - self.main.start_tick) * self.main.params["dt"])
        self.main.angle_velocity = (self.main.angle - self.main.previous_angle) / self.main.params["dt"]
        self.main.angle_acceleration = (self.main.angle_velocity - self.main.previous_angle_velocity) / self.main.params["dt"]
        self.main.full_angle += abs(self.main.angle - self.main.previous_angle)
        self.main.previous_angle = self.main.angle
        self.main.previous_angle_velocity = self.main.angle_velocity

    def step(self):
        if not self.main.stop:
            self.steps[self.main.type]()
            self.normalize_angle()
            self.main.update_targets()

    def normalize_angle(self):
        while self.main.angle < -pi:
            self.main.angle += 2 * pi

        while self.main.angle >= pi:
            self.main.angle -= 2 * pi