import threading
import time
import tkinter as tk
from math import log2

from entities.pendulum import PhysicsPendulum
from tools.parser import Parser
from view.components.inputs.formula_input import FormulaInput


class Engine:
    def __init__(self, entities, model, params):
        self.apply_bottom = None
        self.angle_entry = None
        self.mass_entry = None
        self.time_frame = None
        self.play_pause = None
        self.radiobutton_frame = None
        self.scale_frame = None
        self.control_panel_left = None
        self.button = None
        self.entry = None
        self.entry_frame = None
        self.control_panel_bottom = None
        self.control_panel_right = None
        self.main = None
        self.canvas = None
        self.model = model
        self.params = params
        self.entities = entities
        self.selected_entity = 0
        self.movable_elements = []
        self.root = tk.Tk()
        self.window_width = 1200
        self.window_height = 900
        self.initialize_interface()
        self.id_ch = 1
        self.parser = Parser(self.params["environment"], ["+", "-", "*", "/", " ", "(", ")"])

    def switch_selected(self):
        self.mass_entry.config(state=tk.NORMAL)
        self.length_entry.config(state=tk.NORMAL)
        self.angle_entry.config(state=tk.NORMAL)
        self.name_entry.config(state=tk.NORMAL)
        self.axis_per.config(state=tk.NORMAL)
        self.type_check.config(state=tk.NORMAL)
        self.inertia_moment_fi.set_normal()
        self.mass_per.config(state=tk.ACTIVE)

        if self.params["selected"][1].type == "real":
            self.gamma.config(state=tk.NORMAL)
        else:
            self.gamma.delete(0, tk.END)
            self.gamma.insert(0, "-")
            self.gamma.config(state=tk.DISABLED)

        self.type.set(int(self.params["selected"][1].type == "real"))

        self.mass_entry.delete(0, tk.END)
        self.mass_entry.insert(0, self.params["selected"][1].mass)

        self.length_entry.delete(0, tk.END)
        self.length_entry.insert(0, self.params["selected"][1].size)

        self.angle_entry.delete(0, tk.END)
        self.angle_entry.insert(0, self.params["selected"][1].start_angle)

        self.gamma.delete(0, tk.END)
        self.gamma.insert(0, self.params["selected"][1].gamma)

        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, self.params["selected"][1].name)

        self.name["text"] = self.params["selected"][1].name + "  (" + self.params["selected"][1].id + ")"

        self.axis_per.set(round(self.params["selected"][1].counterweight_size * 100))

        self.inertia_moment_fi.set_normal()
        self.inertia_moment_fi.set_target(self.params["selected"][1].inertia_moment_formula)

        self.mass_per.config(state=tk.NORMAL)
        self.mass_per.set(round(self.params["selected"][1].mass_center_remoteness * 100))

    def set_no_selected(self):
        self.params["selected"][0] = False
        self.params["selected"][1] = None
        self.type.set(0)
        self.type_check.config(state=tk.DISABLED)
        self.mass_entry.delete(0, tk.END)
        self.mass_entry.insert(0, "-")
        self.mass_entry.config(state=tk.DISABLED)

        self.length_entry.delete(0, tk.END)
        self.length_entry.insert(0, "-")
        self.length_entry.config(state=tk.DISABLED)

        self.gamma.delete(0, tk.END)
        self.gamma.insert(0, "-")
        self.gamma.config(state=tk.DISABLED)

        self.angle_entry.delete(0, tk.END)
        self.angle_entry.insert(0, "-")
        self.angle_entry.config(state=tk.DISABLED)

        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, "-")
        self.name_entry.config(state=tk.DISABLED)

        self.name["text"] = "-"

        self.axis_per.set(0)
        self.axis_per.config(state=tk.DISABLED)
        self.type.set(0)
        self.type_check.config(state=tk.DISABLED)
        self.inertia_moment_fi.set_target("-")
        self.inertia_moment_fi.set_disabled()

        self.mass_per.set(0)
        self.mass_per.config(state=tk.DISABLED)

        self.full_angle["text"] = "-"
        self.angle["text"] = "-"
        self.angle_velocity["text"] = "-"
        self.angle_acceleration["text"] = "-"


    def apply(self):
        self.update_model()

    def restart(self):
        self.params["selected"][1].restart()

    def delete(self):
        if self.params["selected"][1] != None:
            self.params["selected"][1].delete()
            self.set_no_selected()

    def update_model(self):
        self.params["selected"][1].mass = float(self.mass_entry.get())
        self.params["selected"][1].size = float(self.length_entry.get())
        self.params["selected"][1].start_angle = float(self.angle_entry.get())
        self.params["selected"][1].name = self.name_entry.get()
        self.params["selected"][1].counterweight_size = float(self.axis_per.get()) / 100
        self.params["selected"][1].gamma = float(self.gamma.get())

        self.params["selected"][1].mass_center_remoteness = float(self.mass_per.get()) / 100
        if self.type.get() == 1:
            self.params["selected"][1].type = "real"
        else:
            self.params["selected"][1].type = "theory"

        self.params["selected"][1].update_targets()

        ok, value = self.inertia_moment_fi.calculate()

        self.params["selected"][1].stop = not ok
        self.params["selected"][1].inertia_moment_formula = self.inertia_moment_fi.get_target_formula()
        if ok:
            self.params["selected"][1].inertia_moment = float(value)

        self.params["selected"][0] = True

    def update_environment(self):
        self.params["environment"]["g"] = float(self.g_entry.get())
        self.params["environment"]["dt"] = float(self.dt_entry.get())

    def update_model_type(self):
        if self.type.get() == 1:
            self.params["selected"][1].type = "real"

            self.gamma.config(state=tk.NORMAL)
            self.gamma.delete(0, tk.END)
            self.gamma.insert(0, self.params["selected"][1].gamma)

        else:
            self.params["selected"][1].type = "theory"

            self.gamma.delete(0, tk.END)
            self.gamma.insert(0, "-")
            self.gamma.config(state=tk.DISABLED)

    def update_axis_per(self, value):
        self.params["selected"][1].counterweight_size = float(value) / 100

    def update_scale(self, value):
        self.params["environment"]["scale"] = 2**float(value)

    def set_play_pause(self):
        self.model.params["stop"] = not self.model.params["stop"]
        if self.model.params["stop"]:
            self.play_pause.config(text="▶")
        else:
            self.play_pause.config(text="◼")

    def add_entity(self):
        pendulum = PhysicsPendulum(self.canvas,  self.params["environment"])
        pendulum.name = "Новый Маятник " + str(self.id_ch)
        pendulum.id = "@p" + str(self.id_ch)
        self.id_ch+=1
        pendulum.view.initialize()

        self.entities[pendulum.id] = pendulum
        self.params["environment"]["model"].entities[pendulum.id] = pendulum

    def initialize(self):
        for key in self.entities:
            self.entities[key].view.initialize()

    def update(self):
        for key in self.entities:
            self.entities[key].view.draw()
        if self.params["selected"][0]:
            self.switch_selected()
            self.params["selected"][0] = False
        if self.params["selected"][1] is not None:
            self.angle["text"] = str(self.params["selected"][1].angle)
            self.full_angle["text"] = str(self.params["selected"][1].full_angle)
            self.angle_velocity["text"] = str(self.params["selected"][1].angle_velocity)
            self.angle_acceleration["text"] = str(self.params["selected"][1].angle_acceleration)
            self.inertia_moment_value["text"] = str(self.params["selected"][1].inertia_moment)
        self.update_environment()
        self.root.after(int(self.params["dt"] * 1000), self.update)

    def initialize_interface(self):
        self.root.title("Pendulums")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_coordinate = (screen_width / 2) - (self.window_width / 2)
        y_coordinate = (screen_height / 2) - (self.window_height / 2)
        self.root.geometry('%dx%d+%d+%d' % (self.window_width, self.window_height, x_coordinate, y_coordinate))

        self.initialize_control_panel_left()
        self.initialize_main()
        self.initialize_control_panel_right()
        self.g_entry.delete(0, tk.END)
        self.g_entry.insert(0, self.params["environment"]["g"])
        self.dt_entry.delete(0, tk.END)
        self.dt_entry.insert(0, self.params["environment"]["dt"])
        self.set_no_selected()

    def initialize_main(self):

        self.main = tk.Canvas(self.root, width=1200, height=600)
        self.main.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.main, width=600, height=600, bg='white')
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.time_frame = tk.Frame(self.canvas, width=100, height=50, bg="white", padx=5, pady=5)
        self.time_frame.pack(side=tk.BOTTOM, anchor=tk.S, fill=tk.NONE)

        self.play_pause = tk.Button(self.time_frame, height=1, width=3, text="▶", command=self.set_play_pause)
        self.play_pause.pack(side=tk.BOTTOM, fill=tk.NONE)

        self.canvas_buttons = tk.Frame(self.canvas, width=100, height=50, bg="white", padx=5, pady=5)
        self.canvas_buttons.pack(side=tk.TOP, anchor=tk.NE, fill=tk.NONE)

        self.add_entity_button = tk.Button(self.canvas_buttons, height=1, width=3, text="+", command=self.add_entity)
        self.add_entity_button.pack(side=tk.TOP, anchor=tk.SE, fill=tk.NONE)

        self.initialize_control_panel_bottom()

    def initialize_control_panel_bottom(self):
        self.control_panel_bottom = tk.Frame(self.main, width=600, height=100)
        self.control_panel_bottom.pack(side=tk.TOP, fill=tk.BOTH)

        environment_frame = tk.LabelFrame(self.control_panel_bottom, height=600, text="Переменные окружения (@env)")
        environment_frame.pack(side=tk.LEFT, fill=tk.BOTH, anchor=tk.NW, padx=5, pady=5)

        g_entry_frame = tk.LabelFrame(environment_frame, height=50, text="УСП (м/c) (.g)")
        g_entry_frame.pack(padx=5, pady=5, side=tk.TOP, fill=tk.X, anchor=tk.W)
        self.g_entry = tk.Entry(g_entry_frame)
        self.g_entry.pack(padx=5, pady=5, side=tk.LEFT, fill=tk.X, expand=True)

        dt_entry_frame = tk.LabelFrame(environment_frame, height=50, text="Дискретизация симуляции (с) (.dt)")
        dt_entry_frame.pack(padx=5, pady=5, side=tk.TOP, fill=tk.X, anchor=tk.W)
        self.dt_entry = tk.Entry(dt_entry_frame)
        self.dt_entry.pack(padx=5, pady=5, side=tk.LEFT, fill=tk.X, expand=True)

        scale_frame = tk.LabelFrame(self.control_panel_bottom, width=100, height=100, text="Масштаб (м = 2^(x) пикс)")
        scale_frame.pack(padx=5, pady=5, side=tk.RIGHT, fill=tk.NONE, anchor=tk.NW)
        self.scale = tk.Scale(scale_frame, orient=tk.HORIZONTAL, from_=-10, to=10, resolution=0.1, command=self.update_scale)
        self.scale.pack(padx=5, pady=5, side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.scale.set(round(log2(self.params["environment"]["scale"]), 2))

    def initialize_control_panel_right(self):
        self.control_panel_right = tk.LabelFrame(self.root, width=300, height=600, padx=10, pady=15,
                                                 text="Настройки маятника")
        self.control_panel_right.pack(side=tk.RIGHT, fill=tk.Y)

        self.name = tk.Label(self.control_panel_right, text="-")
        self.name.pack(side=tk.TOP, anchor=tk.N, fill=tk.BOTH)

        self.state = tk.LabelFrame(self.control_panel_right, width=300, height=600, padx=5, pady=5,
                                                 text="Состояние маятника")
        self.state.pack(side=tk.TOP, fill=tk.X)

        full_angle_container = tk.LabelFrame(self.state, width=300, height=600,
                                        text="Полный угол (рад) (.fa)")
        full_angle_container.pack(side=tk.TOP, fill=tk.X)
        self.full_angle = tk.Label(full_angle_container, text="-", justify="left")
        self.full_angle.pack(side=tk.LEFT, anchor=tk.E, fill=tk.X)

        angle_container = tk.LabelFrame(self.state, width=300, height=600,
                                              text="Угол (рад) (.a)")
        angle_container.pack(side=tk.TOP, fill=tk.X)
        self.angle = tk.Label(angle_container, text="-", justify="left")
        self.angle.pack(side=tk.LEFT, anchor=tk.E, fill=tk.X)

        angle_speed_container = tk.LabelFrame(self.state, width=300, height=600,
                                   text="Угловая скорость (рад/с) (.av)")
        angle_speed_container.pack(side=tk.TOP, fill=tk.X)
        self.angle_velocity = tk.Label(angle_speed_container, text="-", justify="left")
        self.angle_velocity.pack(side=tk.LEFT, anchor=tk.E, fill=tk.X)

        angle_acceleration_container = tk.LabelFrame(self.state, width=300, height=600,
                                        text="Угловое ускорение (рад/(c*с)) (.aa)")
        angle_acceleration_container.pack(side=tk.TOP, fill=tk.X)
        self.angle_acceleration = tk.Label(angle_acceleration_container, text="-", justify="left")
        self.angle_acceleration.pack(side=tk.LEFT, anchor=tk.E, fill=tk.X)

        inertia_moment_container = tk.LabelFrame(self.state, width=300, height=600,
                                                     text="Момент инерции (кг*(м*м)) (.im)")
        inertia_moment_container.pack(side=tk.TOP, fill=tk.X)
        self.inertia_moment_value = tk.Label(inertia_moment_container, text="-", justify="left")
        self.inertia_moment_value.pack(side=tk.LEFT, anchor=tk.E, fill=tk.X)

        self.parameters_container = tk.LabelFrame(self.control_panel_right, width=200, padx=10, pady=10,
                                                  text="Параметры")
        self.parameters_container.pack(side=tk.TOP, anchor=tk.N, fill=tk.BOTH)

        self.name_entry = tk.Entry(self.parameters_container)
        self.name_entry.insert(0, self.name["text"])
        self.name_entry.pack(side=tk.TOP, anchor=tk.N, fill=tk.BOTH)

        self.type = tk.IntVar(value=1)
        self.type_check = tk.Checkbutton(self.parameters_container, text="Полная симуляция", variable=self.type,
                                   command=self.update_model_type, justify="left")
        self.type_check.pack(side=tk.TOP, fill=tk.X, expand=True)

        mass_entry_frame = tk.LabelFrame(self.parameters_container, height=100, text="Масса (кг) (.m)")
        mass_entry_frame.pack(side=tk.TOP, fill=tk.BOTH, anchor=tk.N)
        self.mass_entry = tk.Entry(mass_entry_frame)
        self.mass_entry.pack(padx=5, pady=5, side=tk.LEFT, fill=tk.X, expand=True)

        length_entry_frame = tk.LabelFrame(self.parameters_container, height=100, text="Длина (м) (.r)")
        length_entry_frame.pack(side=tk.TOP, fill=tk.BOTH, anchor=tk.N)
        self.length_entry = tk.Entry(length_entry_frame)
        self.length_entry.pack(padx=5, pady=5, side=tk.LEFT, fill=tk.X, expand=True)

        angle_entry_frame = tk.LabelFrame(self.parameters_container, height=100, text="Начальный угол отклонения (рад)")
        angle_entry_frame.pack(side=tk.TOP, fill=tk.BOTH, anchor=tk.N)
        self.angle_entry = tk.Entry(angle_entry_frame)
        self.angle_entry.pack(padx=5, pady=5, side=tk.LEFT, fill=tk.X, expand=True)

        axis_per_frame = tk.LabelFrame(self.parameters_container, height=600, text="Растояние до оси (%) (.rp)")
        axis_per_frame.pack(side=tk.TOP, fill=tk.BOTH, anchor=tk.N)
        self.axis_per = tk.Scale(axis_per_frame, orient=tk.HORIZONTAL, from_=0, to=100, resolution=1, command=self.update_axis_per)
        self.axis_per.pack(padx=5, pady=5, side=tk.LEFT, fill=tk.X, expand=True)

        mass_per_frame = tk.LabelFrame(self.parameters_container, height=600, text="Растояние до центра масс (%) (.rmp)")
        mass_per_frame.pack(side=tk.TOP, fill=tk.BOTH, anchor=tk.N)
        self.mass_per = tk.Scale(mass_per_frame, orient=tk.HORIZONTAL, from_=0, to=100, resolution=1, state=tk.DISABLED)
        self.mass_per.pack(padx=5, pady=5, side=tk.LEFT, fill=tk.X, expand=True)


        length_entry_frame = tk.LabelFrame(self.parameters_container, height=600, text="Формула момента инерции")
        length_entry_frame.pack(side=tk.TOP, fill=tk.BOTH, anchor=tk.N)
        inertia_moment_entry = tk.Entry(length_entry_frame, state=tk.DISABLED)
        inertia_moment_entry.pack(padx=5, pady=5, side=tk.LEFT, fill=tk.X, expand=True)

        self.inertia_moment_fi = FormulaInput(self.params, Parser(self.params, ["+", "-", "*", "/", " ", "(", ")"]), inertia_moment_entry)

        gamma_frame = tk.LabelFrame(self.parameters_container, height=600,
                                       text="Коофициент вязкого трения (ед)")
        gamma_frame.pack(side=tk.TOP, fill=tk.BOTH, anchor=tk.N)
        self.gamma = tk.Entry(gamma_frame)
        self.gamma.pack(padx=5, pady=5, side=tk.LEFT, fill=tk.X, expand=True)

        self.apply_bottom = tk.Button(self.control_panel_right, width=10, text="Применить", command=self.apply)
        self.apply_bottom.pack(side=tk.TOP, anchor=tk.N, fill=tk.BOTH)
        self.restart_bottom = tk.Button(self.control_panel_right, width=10, text="Перезапустить", command=self.restart)
        self.restart_bottom.pack(side=tk.TOP, anchor=tk.N, fill=tk.BOTH)
        self.delete_bottom = tk.Button(self.control_panel_right, width=10, text="Удалить", command=self.delete)
        self.delete_bottom.pack(side=tk.BOTTOM, anchor=tk.N, fill=tk.BOTH)

    def initialize_control_panel_left(self):
        self.control_panel_left = tk.Frame(self.root, width=300, height=600, padx=10, pady=10)
        self.control_panel_left.pack(side=tk.LEFT, fill=tk.Y)

        self.graphs = tk.Frame(self.control_panel_left, width=300, height=600)
        self.graphs.pack(side=tk.TOP, anchor=tk.N)



    def run(self):
        self.initialize()
        self.root.after(0, self.update)
        self.root.mainloop()
