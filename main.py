import signal
import threading

from entities.pendulum import PhysicsPendulum
from entities.point import Point2D
from model.engine import Engine as ModelEngine
from tools.closer import Closer
from view.engine import Engine as ViewEngine

model_engine = ModelEngine([],  {"dt": 0.01, "stop": False})
view_engine = ViewEngine([], model_engine, {"dt": 0.01, "stop": False})

pendulum = PhysicsPendulum(view_engine.canvas, {"dt": 0.01, "g": 10, "scale": 100})
model_engine.entities.append(pendulum)
view_engine.entities.append(pendulum)

model_tread = threading.Thread(target=model_engine.run)

closer = Closer(view_engine.root, [model_tread])
view_engine.root.protocol("WM_DELETE_WINDOW", closer.close)
model_engine.params["closer"] = closer

model_tread.start()

view_engine.run()
