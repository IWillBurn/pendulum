import signal
import threading

from entities.pendulum import PhysicsPendulum
from entities.point import Point2D
from model.engine import Engine as ModelEngine
from tools.closer import Closer
from view.engine import Engine as ViewEngine

selected = [True, None]
environment = {"dt": 0.01, "g": 10, "scale": 100, "selected": selected}

model_engine = ModelEngine([],  {"stop": True, "environment": environment})
view_engine = ViewEngine([], model_engine, {"dt": 0.001, "stop": True, "selected": selected, "environment": environment})

pendulum1 = PhysicsPendulum(view_engine.canvas, environment)
pendulum1.name = "Маятник A"
model_engine.entities.append(pendulum1)
view_engine.entities.append(pendulum1)
selected[1] = pendulum1

pendulum2 = PhysicsPendulum(view_engine.canvas, environment)
pendulum2.name = "Маятник B"

model_engine.entities.append(pendulum2)
view_engine.entities.append(pendulum2)

model_tread = threading.Thread(target=model_engine.run)

closer = Closer(view_engine.root, [model_tread])
view_engine.root.protocol("WM_DELETE_WINDOW", closer.close)
model_engine.params["closer"] = closer

model_tread.start()

view_engine.run()
