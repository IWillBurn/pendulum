import threading
import time


class Engine:
    def __init__(self, entities, params):
        self.entities = entities
        self.params = params

    def update(self):
        for entity in self.entities:
            entity.model.step()

    def run(self):
        while not self.params["closer"].is_closed:
            time.sleep(self.params["environment"]["dt"])
            if self.params["stop"]:
                continue
            self.update()
