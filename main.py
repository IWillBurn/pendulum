import signal
import threading

from entities.environment import Environment
from entities.line_graph import LineGraph
from entities.pendulum import PhysicsPendulum
from entities.point import Point2D
from model.engine import Engine as ModelEngine
from tools.closer import Closer
from view.engine import Engine as ViewEngine

selected = [False, None]
environment = {"dt": 0.01, "g": 10, "scale": 100, "selected": selected, "model_tick": 0}

model_engine = ModelEngine({},  {"stop": True, "environment": environment})
view_engine = ViewEngine({}, model_engine, {"dt": 0.001, "stop": True, "selected": selected, "environment": environment})

environment["model"] = model_engine
environment["view"] = view_engine

graph1 = LineGraph(view_engine.graphs, environment, "(@p1.fa - @p2.fa) / (@env.mt / @env.dt)")
view_engine.entities["@g1"] = graph1

graph2 = LineGraph(view_engine.graphs, environment, "@p2.a")
view_engine.entities["@g2"] = graph2

env = Environment(environment)
model_engine.entities["@env"] = env
view_engine.entities["@env"] = env

model_tread = threading.Thread(target=model_engine.run)

closer = Closer(view_engine.root, [model_tread])
view_engine.root.protocol("WM_DELETE_WINDOW", closer.close)
model_engine.params["closer"] = closer

model_tread.start()

view_engine.run()
