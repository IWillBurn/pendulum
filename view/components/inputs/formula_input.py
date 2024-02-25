import tkinter as tk
class FormulaInput:
    def __init__(self, params, parser, entry):
        self.entry = entry
        self.params = params
        self.target = ""
        self.parser = parser
        self.target_value = 0
        self.initialize()

    def initialize(self):
        self.entry.insert(0, self.target)

    def get_target_formula(self):
        return self.entry.get()

    def calculate(self):
        self.target = self.get_target_formula()
        ok, self.target_value = self.parser.calculate_target(self.target)
        if ok:
            self.entry.config(bg="white")
        else:
            self.entry.config(bg="#FF5555")
        return ok, self.target_value

    def set_target(self, target):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, target)

    def set_normal(self):
        self.entry.config(state=tk.NORMAL)

    def set_disabled(self):
        self.entry.config(state=tk.DISABLED)