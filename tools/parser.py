from tools.floats import is_number


class Parser:
    def __init__(self, params, tokens):
        self.params = params
        self.tokens = tokens

    def calculate_target(self, target):
        if target == "":
            return False, 0
        value = ""
        command = ""
        for ch in target:
            is_token = False
            for token in self.tokens:
                if ch == token:
                    if value != "":
                        ok, result = self.calculate_value(value)
                        if not ok:
                            return False, 0
                        command += "(" + str(result) + ")"
                    value = ""
                    command += str(ch)
                    is_token = True
                    break
            if not is_token:
                value += ch
        if value != "":
            ok, result = self.calculate_value(value)
            if not ok:
                return False, 0
            if result > 0:
                command += str(result)
            else:
                command += "(" + str(result) + ")"
        try:
            target_value = eval(command)
            return True, target_value
        except:
            return False, 0

    def calculate_value(self, value_code):
        if is_number(value_code):
            return True, float(value_code)
        try:
            entity, target_name = value_code.split(".")
        except ValueError:
            return False, 0
        if not (entity in self.params["model"].entities and target_name in self.params["model"].entities[entity].targets):
            return False, 0
        return True, self.params["model"].entities[entity].targets[target_name].value
