from tools.target import Target


class Environment:
    def __init__(self, main):
        self.main = main

    def step(self):
        self.main.targets = {"dt": Target(self.main.data_targets["dt"]), "g": Target(self.main.data_targets["g"]), "mt": Target(self.main.data_targets["model_tick"])}
