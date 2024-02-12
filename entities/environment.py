from math import pi
from xml.dom.minidom import Entity

from tools.target import Target
from tools.vector import Vector2

from model.behaviours.environment import Environment as EnvironmentModel
from view.behaviours.environment import Environment as EnvironmentView


class Environment:
    def __init__(self, targets):
        self.data_targets = targets
        self.targets = {"dt": Target(targets["dt"]), "g": Target(targets["g"]), "mt": Target(targets["model_tick"])}
        self.model = EnvironmentModel(self)
        self.view = EnvironmentView(self)