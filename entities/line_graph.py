from view.components.graph.line import Line


class LineGraph:
    def __init__(self, canvas, params, target):
        self.view = Line(canvas, params, target)
