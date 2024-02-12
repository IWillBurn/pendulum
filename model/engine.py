import threading
import time


class Engine:
    def __init__(self, entities, params):
        self.entities = entities
        self.params = params

    def update(self):
        for key in self.entities:
            self.entities[key].model.step()

    def run(self):
        while not self.params["closer"].is_closed:
            time.sleep(self.params["environment"]["dt"])
            if self.params["stop"]:
                continue
            self.params["environment"]["model_tick"] += 1
            self.update()
