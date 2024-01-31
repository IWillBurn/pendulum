from tools.vector import Vector2


class Point2D:
    def __init__(self, main):
        self.main = main

    def step(self):
        self.main.velocity.add(self.main.acceleration.multiply_to_scalar_value(self.main.params["dt"]))
        self.main.position.add(self.main.velocity.multiply_to_scalar_value(self.main.params["dt"]))

