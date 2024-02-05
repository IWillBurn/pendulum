import threading
import time
import tkinter as tk


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

    def switch_selected(self):
        self.mass_entry.delete(0, tk.END)
        self.mass_entry.insert(0, self.params["selected"][1].mass)

        self.length_entry.delete(0, tk.END)
        self.length_entry.insert(0, self.params["selected"][1].size)

        self.angle_entry.delete(0, tk.END)
        self.angle_entry.insert(0, self.params["selected"][1].angle)

        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, self.params["selected"][1].name)

        self.name.text = self.params["selected"][1].name

        self.name["text"] = self.params["selected"][1].name

        self.axis_per.set(round(self.params["selected"][1].counterweight_size * 100))

    def update_model(self):

        self.params["selected"][1].mass = float(self.mass_entry.get())
        self.params["selected"][1].size = float(self.length_entry.get())
        self.params["selected"][1].angle = float(self.angle_entry.get())
        self.params["selected"][1].name = self.name_entry.get()
        self.params["selected"][1].counterweight_size = float(self.axis_per.get()) / 100
        self.params["selected"][0] = True

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

    def initialize(self):
        for entity in self.entities:
            entity.view.initialize()

    def update(self):
        for entity in self.entities:
            entity.view.draw()
        if self.params["selected"][0]:
            self.switch_selected()
            self.params["selected"][0] = False
        self.root.after(int(self.params["dt"] * 1000), self.update)

    def initialize_interface(self):
        self.root.title("Drawing Application")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_coordinate = (screen_width / 2) - (self.window_width / 2)
        y_coordinate = (screen_height / 2) - (self.window_height / 2)
        self.root.geometry('%dx%d+%d+%d' % (self.window_width, self.window_height, x_coordinate, y_coordinate))

        self.initialize_control_panel_left()
        self.initialize_main()
        self.initialize_control_panel_right()

    def initialize_main(self):

        self.main = tk.Canvas(self.root, width=1200, height=600)
        self.main.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.main, width=600, height=600, bg='white')
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.time_frame = tk.Frame(self.canvas, width=100, height=50, bg="white", padx=5, pady=5)
        self.time_frame.pack(side=tk.BOTTOM, anchor=tk.S, fill=tk.NONE)

        self.play_pause = tk.Button(self.time_frame, height=1, width=3, text="▶", command=self.set_play_pause)
        self.play_pause.pack(side=tk.BOTTOM, fill=tk.NONE)

        self.initialize_control_panel_bottom()

    def initialize_control_panel_bottom(self):
        self.control_panel_bottom = tk.Frame(self.main, width=600, height=100)
        self.control_panel_bottom.pack(side=tk.TOP, fill=tk.BOTH)

        environment_frame = tk.LabelFrame(self.control_panel_bottom, height=600, text="Переменные окружения")
        environment_frame.pack(side=tk.LEFT, fill=tk.BOTH, anchor=tk.NW, padx=5, pady=5)

        g_entry_frame = tk.LabelFrame(environment_frame, height=50, text="Ускорение свободного падения (м/c)")
        g_entry_frame.pack(padx=5, pady=5, side=tk.TOP, fill=tk.X, anchor=tk.W)
        self.g_entry = tk.Entry(g_entry_frame)
        self.g_entry.pack(padx=5, pady=5, side=tk.LEFT, fill=tk.X, expand=True)

        dt_entry_frame = tk.LabelFrame(environment_frame, height=50, text="Дискретизация симуляции (с)")
        dt_entry_frame.pack(padx=5, pady=5, side=tk.TOP, fill=tk.X, anchor=tk.W)
        self.dt_entry = tk.Entry(dt_entry_frame)
        self.dt_entry.pack(padx=5, pady=5, side=tk.LEFT, fill=tk.X, expand=True)

        scale_frame = tk.LabelFrame(self.control_panel_bottom, width=100, height=100, text="Масштаб")
        scale_frame.pack(padx=5, pady=5, side=tk.RIGHT, fill=tk.NONE, anchor=tk.NW)
        self.scale = tk.Scale(scale_frame, orient=tk.HORIZONTAL, from_=-10, to=10, resolution=0.1, command=self.update_scale)
        self.scale.pack(padx=5, pady=5, side=tk.RIGHT)

    def initialize_control_panel_right(self):
        self.control_panel_right = tk.LabelFrame(self.root, width=300, height=600, padx=10, pady=15,
                                                 text="Настройки маятника")
        self.control_panel_right.pack(side=tk.RIGHT, fill=tk.Y)

        self.name = tk.Label(self.control_panel_right, text="-")
        self.name.pack(side=tk.TOP, anchor=tk.N, fill=tk.BOTH)

        self.state = tk.LabelFrame(self.control_panel_right, width=300, height=600, padx=5, pady=5,
                                                 text="Состояние маятника")
        self.state.pack(side=tk.TOP, fill=tk.X)

        angle_container = tk.LabelFrame(self.state, width=300, height=600,
                                              text="Угол")
        angle_container.pack(side=tk.TOP, fill=tk.X)
        self.angle = tk.Label(angle_container, text="-", justify="left")
        self.angle.pack(side=tk.LEFT, anchor=tk.E, fill=tk.X)

        angle_speed_container = tk.LabelFrame(self.state, width=300, height=600,
                                   text="Угловая скорость")
        angle_speed_container.pack(side=tk.TOP, fill=tk.X)
        self.angle_speed = tk.Label(angle_speed_container, text="-", justify="left")
        self.angle_speed.pack(side=tk.LEFT, anchor=tk.E, fill=tk.X)

        angle_acceleration_container = tk.LabelFrame(self.state, width=300, height=600,
                                        text="Угловое ускорение")
        angle_acceleration_container.pack(side=tk.TOP, fill=tk.X)
        self.angle_acceleration = tk.Label(angle_acceleration_container, text="-", justify="left")
        self.angle_acceleration.pack(side=tk.LEFT, anchor=tk.E, fill=tk.X)

        """
        self.pendulum_container = tk.LabelFrame(self.control_panel_right, width=200, height=200, padx=10, pady=10,
                                                text="Маятник")
        self.pendulum_container.pack(side=tk.TOP, anchor=tk.N, fill=tk.BOTH)
        self.pendulum_image = tk.Frame(self.pendulum_container, width=200, height=200, padx=10, pady=10, bg="white")
        self.pendulum_image.pack(side=tk.TOP, anchor=tk.N, fill=tk.BOTH)
        """

        self.parameters_container = tk.LabelFrame(self.control_panel_right, width=200, padx=10, pady=10,
                                                  text="Параметры")
        self.parameters_container.pack(side=tk.TOP, anchor=tk.N, fill=tk.BOTH)

        self.name_entry = tk.Entry(self.parameters_container)
        self.name_entry.insert(0, self.name["text"])
        self.name_entry.pack(side=tk.TOP, anchor=tk.N, fill=tk.BOTH)

        mass_entry_frame = tk.LabelFrame(self.parameters_container, height=100, text="Масса (кг)")
        mass_entry_frame.pack(side=tk.TOP, fill=tk.BOTH, anchor=tk.N)
        self.mass_entry = tk.Entry(mass_entry_frame)
        self.mass_entry.pack(padx=5, pady=5, side=tk.LEFT, fill=tk.X, expand=True)

        length_entry_frame = tk.LabelFrame(self.parameters_container, height=100, text="Длина (м)")
        length_entry_frame.pack(side=tk.TOP, fill=tk.BOTH, anchor=tk.N)
        self.length_entry = tk.Entry(length_entry_frame)
        self.length_entry.pack(padx=5, pady=5, side=tk.LEFT, fill=tk.X, expand=True)

        angle_entry_frame = tk.LabelFrame(self.parameters_container, height=100, text="Начальный угол отклонения (рад)")
        angle_entry_frame.pack(side=tk.TOP, fill=tk.BOTH, anchor=tk.N)
        self.angle_entry = tk.Entry(angle_entry_frame)
        self.angle_entry.pack(padx=5, pady=5, side=tk.LEFT, fill=tk.X, expand=True)

        axis_per_frame = tk.LabelFrame(self.parameters_container, height=600, text="Растояние до оси (%)")
        axis_per_frame.pack(side=tk.TOP, fill=tk.BOTH, anchor=tk.N)
        self.axis_per = tk.Scale(axis_per_frame, orient=tk.HORIZONTAL, from_=0, to=100, resolution=1, command=self.update_axis_per)
        self.axis_per.pack(padx=5, pady=5, side=tk.LEFT, fill=tk.X, expand=True)

        inertia_moment_frame = tk.LabelFrame(self.parameters_container, height=600, text="Момент инерции")
        inertia_moment_frame.pack(side=tk.TOP, fill=tk.BOTH, anchor=tk.N)

        lang = tk.StringVar(value="1")

        self.inertia_moment_math = tk.Radiobutton(inertia_moment_frame, value="1", text="Математический", variable=lang)
        self.inertia_moment_math.pack(padx=5, pady=2, side=tk.TOP, anchor=tk.W)
        self.inertia_moment_tube = tk.Radiobutton(inertia_moment_frame, value="2", text="Тонкостенный стержень",
                                                  variable=lang)
        self.inertia_moment_tube.pack(padx=5, pady=2, side=tk.TOP, anchor=tk.W)
        self.inertia_moment_custom = tk.Radiobutton(inertia_moment_frame, value="3", text="Свободный", variable=lang)
        self.inertia_moment_custom.pack(padx=5, pady=2, side=tk.TOP, anchor=tk.W)

        mass_per_frame = tk.LabelFrame(inertia_moment_frame, height=600, text="Растояние до центра масс (%)")
        mass_per_frame.pack(side=tk.TOP, fill=tk.BOTH, anchor=tk.N)
        self.mass_per = tk.Scale(mass_per_frame, orient=tk.HORIZONTAL, from_=1, to=100, resolution=1, state=tk.DISABLED)
        self.mass_per.pack(padx=5, pady=5, side=tk.LEFT, fill=tk.X, expand=True)

        length_entry_frame = tk.LabelFrame(inertia_moment_frame, height=600, text="Момент инерции (кг*м*м)")
        length_entry_frame.pack(side=tk.TOP, fill=tk.BOTH, anchor=tk.N)
        self.inertia_moment_entry = tk.Entry(length_entry_frame, state=tk.DISABLED)
        self.inertia_moment_entry.pack(padx=5, pady=5, side=tk.LEFT, fill=tk.X, expand=True)

        self.apply_bottom = tk.Button(self.control_panel_right, width=10, text="Применить", command=self.update_model)
        self.apply_bottom.pack(side=tk.TOP, anchor=tk.N, fill=tk.BOTH)
        self.apply_bottom = tk.Button(self.control_panel_right, width=10, text="Сбросить изменения", command=self.update_model)
        self.apply_bottom.pack(side=tk.TOP, anchor=tk.N, fill=tk.BOTH)

    def initialize_control_panel_left(self):
        self.control_panel_left = tk.Frame(self.root, width=300, height=600, padx=10, pady=10)
        self.control_panel_left.pack(side=tk.LEFT, fill=tk.NONE)

        self.entry_frame = tk.Frame(self.control_panel_left, width=300, height=600)
        self.entry_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        label = tk.Label(self.entry_frame, text="Поле для ввода!", justify=tk.LEFT)
        label.pack(pady=0, side=tk.TOP, fill=tk.NONE)

        entry = tk.Entry(self.entry_frame, width=20)
        entry.pack(pady=5, side=tk.LEFT, fill=tk.NONE)

        button = tk.Button(self.entry_frame, width=10, text="Button 1")
        button.pack(pady=5, side=tk.RIGHT, fill=tk.NONE)

        self.entry_frame = tk.Frame(self.control_panel_left, width=100, height=600)
        self.entry_frame.pack(side=tk.BOTTOM, fill=tk.NONE)

        label = tk.Label(self.entry_frame, text="Поле для ввода!")
        label.pack(pady=0, side=tk.TOP, fill=tk.NONE)

        entry = tk.Entry(self.entry_frame, width=20)
        entry.insert(tk.END, "1")
        entry.pack(pady=5, side=tk.LEFT, fill=tk.NONE)

        button = tk.Button(self.entry_frame, height=1, width=3, text="▶")
        button.pack(pady=5, side=tk.RIGHT, fill=tk.NONE)

    def run(self):
        self.initialize()
        self.root.after(0, self.update)
        self.root.mainloop()
