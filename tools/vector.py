import math


class Vector2:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def size(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def add(self, delta):
        self.x += delta.x
        self.y += delta.y

    def multiply_to_scalar(self, value):
        self.x *= value
        self.y *= value

    def multiply_to_scalar_value(self, value):
        return Vector2(self.x * value, self.y * value)
