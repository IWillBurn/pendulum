from math import log2

from tools.floats import is_number
from tools.vector import Vector2
import tkinter as tk


class Line:
    def __init__(self, container, params, target):
        self.target = target
        self.container = container
        self.canvas = None
        self.params = params
        self.points_size = 100
        self.points = []
        self.pool_size = 100
        self.pool = []
        self.graph = []
        self.colors = ["red", "green", "blue", "orange", "black"]
        self.colors_mask = [False, False, False, False, False]
        self.x_scale = 1
        self.y_scale = 6.6
        self.need_update = False
        self.draw_start_x = 200
        self.draw_start_y = 100
        self.draw_min_y = 0
        self.draw_max_y = 0
        self.draw_axis_y = 0
        self.disc = 5
        self.start_tick = 0
        self.current_tick = 0
        self.is_auto = tk.BooleanVar(value=True)
        self.scale_type = "center"
        self.scale_type_changed = False
        self.pause = True
        self.focus_behaviours = {"center": self.center_behaviour, "axis_up": self.axis_up_behaviour, "axis_down": self.axis_down_behaviour, "custom": self.custom_behaviour}
        self.tokens = ["+", "-", "*", "/", " ", "(", ")"]

    def change_x_scale(self, value):
        self.x_scale = float(value)
        self.refresh()

    def change_y_scale(self, value):
        self.y_scale = float(value)
        self.refresh()

    def switch_auto(self):
        if self.is_auto.get():
            if self.focus_type_var.get() != "custom":
                self.graph_scale_y.config(state=tk.DISABLED)
            else:
                self.graph_scale_y.config(state=tk.NORMAL)
        else:
            self.graph_scale_y.config(state=tk.ACTIVE)

    def change_coords(self, event):

        x = (event.x - self.draw_start_x) / self.x_scale / 100
        y = - (event.y - self.draw_start_y) / 2 ** self.y_scale + self.draw_axis_y

        self.coords.config(
            text="(" + str(round(x, 5)) + ";" + str(round(y, 5)) + ")")

    def calculate_target(self, target):
        if target == "":
            return False, 0
        value = ""
        self.command = ""
        for ch in target:
            is_token = False
            for token in self.tokens:
                if ch == token:
                    if value != "":
                        ok, result = self.calculate_value(value)
                        if not ok:
                            return False, 0
                        self.command += "(" + str(result) + ")"
                    value = ""
                    self.command += str(ch)
                    is_token = True
                    break
            if not is_token:
                value += ch
        if value != "":
            ok, result = self.calculate_value(value)
            if not ok:
                return False, 0
            if result > 0:
                self.command += str(result)
            else:
                self.command += "(" + str(result) + ")"
        try:
            target_value = eval(self.command)
            return True, target_value
        except:
            return False, 0

    def calculate_value(self, value_code):
        current_value = 0
        if is_number(value_code):
            return True, float(value_code)
        try:
            entity, target_name = value_code.split(".")
        except ValueError:
            return False, 0
        if not (entity in self.params["model"].entities and target_name in self.params["model"].entities[
            entity].targets):
            return False, 0
        return True, self.params["model"].entities[entity].targets[target_name].value

    def update_target(self):
        self.target = self.target_entry.get()

    def switch_type(self):
        self.scale_type = self.focus_type_var.get()
        self.scale_type_changed = True

    def initialize(self):

        self.start_tick = self.params["model_tick"]
        self.graph_container = tk.LabelFrame(self.container, width=300, height=400)
        self.graph_container.pack(side=tk.TOP, fill=tk.NONE)
        self.canvas = tk.Canvas(self.graph_container, width=200, height=200, bg="white")
        self.canvas.pack(side=tk.TOP, anchor=tk.N)

        self.canvas.bind('<Motion>', self.change_coords)

        self.zero_line = self.canvas.create_line(self.draw_start_x - 200, self.draw_start_y, self.draw_start_x,
                                                 self.draw_start_y, width=1, fill="gray")
        self.zero_lable = self.canvas.create_text(self.draw_start_x - 190, self.draw_start_y + 8, text="0",
                                                  font=("Arial", 8), fill="gray", justify=tk.LEFT, anchor=tk.W)

        self.max_line = self.canvas.create_line(self.draw_start_x - 200, self.draw_start_y + 90, self.draw_start_x,
                                                self.draw_start_y + 90, width=1, fill="gray")
        self.max_lable = self.canvas.create_text(self.draw_start_x - 190, self.draw_start_y - 82, text="0.5",
                                                 font=("Arial", 8), fill="gray", justify=tk.LEFT, anchor=tk.W)

        self.min_line = self.canvas.create_line(self.draw_start_x - 200, self.draw_start_y - 90, self.draw_start_x,
                                                self.draw_start_y - 90, width=1, fill="gray")
        self.min_lable = self.canvas.create_text(self.draw_start_x - 190, self.draw_start_y + 98, text="-0.5",
                                                 font=("Arial", 8), fill="gray", justify=tk.LEFT, anchor=tk.W)

        self.coords = tk.Label(self.graph_container, text="(0; 0)")
        self.coords.pack(side=tk.TOP, fill=tk.X)

        self.target_entry = tk.Entry(self.graph_container)
        self.target_entry.pack(side=tk.TOP, fill=tk.X)

        graph_scales_container = tk.Frame(self.graph_container)
        graph_scales_container.pack(side=tk.TOP, fill=tk.X)

        self.graph_scale_x = tk.Scale(graph_scales_container, orient=tk.HORIZONTAL, from_=0.4, to=2, resolution=0.1,
                                      command=self.change_x_scale)
        self.graph_scale_x.pack(padx=5, pady=5, side=tk.LEFT, fill=tk.X, expand=True)

        self.graph_scale_y = tk.Scale(graph_scales_container, orient=tk.HORIZONTAL, from_=-10, to=10, resolution=0.1,
                                      command=self.change_y_scale)
        self.graph_scale_y.pack(padx=5, pady=5, side=tk.LEFT, fill=tk.X, expand=True)

        auto_container = tk.LabelFrame(self.graph_container, text="Настройки автофокуса")
        auto_container.pack(side=tk.TOP, fill=tk.X, expand=True)

        self.auto = tk.Checkbutton(auto_container, text="автофокус вкл", variable=self.is_auto,
                                   command=self.switch_auto)
        self.auto.pack(side=tk.TOP, fill=tk.X, expand=True)

        self.focus_type_var = tk.StringVar(value="center")

        self.focus_type_container = tk.LabelFrame(auto_container, text="Позиция абциссы")
        self.focus_type_container.pack(side=tk.TOP, fill=tk.X, expand=True)

        self.focus_type_radio_center = tk.Radiobutton(self.focus_type_container, text="центр", variable=self.focus_type_var, value="center", command=self.switch_type)
        self.focus_type_radio_center.pack(side=tk.LEFT, expand=True)

        self.focus_type_axis_down = tk.Radiobutton(self.focus_type_container, text="верх",
                                                   variable=self.focus_type_var, value="axis_down",
                                                   command=self.switch_type)
        self.focus_type_axis_down.pack(side=tk.LEFT, expand=True)

        self.focus_type_radio_axis_up = tk.Radiobutton(self.focus_type_container, text="низ",
                                                variable=self.focus_type_var, value="axis_up", command=self.switch_type)
        self.focus_type_radio_axis_up.pack(side=tk.LEFT, expand=True)

        self.focus_type_custom = tk.Radiobutton(self.focus_type_container, text="нет",
                                                variable=self.focus_type_var, value="custom", command=self.switch_type)
        self.focus_type_custom.pack(side=tk.LEFT, expand=True)

        self.graph_scale_y.set(self.y_scale)
        self.graph_scale_x.set(self.x_scale)
        self.graph_scale_y.config(state=tk.DISABLED)
        self.target_entry.insert(0, self.target)

        for i in range(self.pool_size):
            line = self.canvas.create_line(-10, -10, -20, -20, width=3, fill="black")
            self.pool.append(line)

    def refresh(self):
        if self.focus_type_var.get() != "custom":
            self.graph_scale_y.config(state=tk.DISABLED)
        else:
            self.graph_scale_y.config(state=tk.NORMAL)
        # self.canvas.coords(self.zero_line)
        self.refresh_zero_line()
        self.refresh_max_line()
        self.refresh_min_line()
        for line in self.graph:
            self.canvas.coords(line, -10, -10, -20, -20)
        count_of_lines = len(self.graph)
        for i in range(count_of_lines):
            line = self.graph.pop(0)
            self.pool.append(line)
        for i in range(len(self.points) - 1):
            line = self.pool.pop(0)
            self.graph.append(line)
            start_x = self.draw_start_x + (self.points[i].x - self.current_tick) * self.x_scale
            start_y = self.draw_start_y - (self.points[i].y - self.draw_axis_y) * 2 ** self.y_scale
            end_x = self.draw_start_x + (self.points[i + 1].x - self.current_tick) * self.x_scale
            end_y = self.draw_start_y - (self.points[i + 1].y - self.draw_axis_y) * 2 ** self.y_scale
            self.canvas.coords(line, start_x, start_y, end_x, end_y)

    def refresh_zero_line(self):
        start_x = 0
        end_x = self.draw_start_x
        y = self.draw_start_y + self.draw_axis_y * 2 ** self.y_scale
        self.canvas.coords(self.zero_line, start_x, y, end_x, y)
        self.canvas.coords(self.zero_lable, start_x + 30, y + 8)

    def refresh_max_line(self):
        y = - (10 - self.draw_start_y) / 2 ** self.y_scale + self.draw_axis_y
        self.canvas.itemconfig(self.max_lable, text=round(y, 2))

    def refresh_min_line(self):
        y = - (190 - self.draw_start_y) / 2 ** self.y_scale + self.draw_axis_y
        self.canvas.itemconfig(self.min_lable, text=round(y, 2))

    def center_behaviour(self, max_y, min_y):
        self.draw_axis_y = 0
        if max_y != 0 and min_y != 0:
            self.y_scale = log2(min(abs(100 / max_y), abs(100 / min_y)) * 2 / 3)
        else:
            self.y_scale = 1

    def axis_up_behaviour(self, max_y, min_y):
        self.draw_axis_y = max_y / 2
        self.y_scale = log2(abs(200 / max_y) * 2 / 3)

    def axis_down_behaviour(self, max_y, min_y):
        self.draw_axis_y = min_y / 2
        self.y_scale = log2(abs(200 / min_y) * 2 / 3)

    def custom_behaviour(self, max_y, min_y):
        self.draw_axis_y = (min_y + max_y) / 2
        if min_y != max_y:
            self.graph_scale_y.config(to=log2(abs(200 / abs(min_y - max_y)) * 2 / 3))
        if self.scale_type_changed:
            self.y_scale = log2(abs(200 / abs(min_y - max_y)) * 2 / 3)

    def refresh_with_scale(self):
        max_x = 0
        max_y = 0
        if self.is_auto.get():
            flag = True
            max_y = -1
            min_y = -1
            for point in self.points:
                if flag:
                    max_y = point.y
                    min_y = point.y
                    flag = False
                    continue
                if max_y < point.y:
                    max_y = point.y
                if min_y > point.y:
                    min_y = point.y
            if max_y != 0 and min_y != 0:
                self.focus_behaviours[self.scale_type](max_y, min_y)
                self.graph_scale_y.config(state=tk.ACTIVE)
                self.graph_scale_y.set(self.y_scale)
                self.graph_scale_y.config(state=tk.DISABLED)
        self.scale_type_changed = False
        self.refresh()

    def add(self, point):
        self.points.append(point)
        self.refresh_with_scale()

        if len(self.points) > self.points_size or len(self.pool) == 0:
            self.points.pop(0)
            line = self.graph.pop(0)
            self.pool.append(line)
            self.canvas.coords(self.pool[-1], -10, -10, -20, -20)
        self.need_update = True

    def draw(self):
        if self.params["model_tick"] % self.disc == 0 and self.params["model_tick"] != self.current_tick:
            self.update_target()
            ok, target_value = self.calculate_target(self.target)
            if ok:
                self.current_tick = self.params["model_tick"]
                self.add(Vector2(self.current_tick, target_value))
