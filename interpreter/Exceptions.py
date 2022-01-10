class ReturnValueException(Exception):
    def __init__(self, value):
        self.value = value


class BreakException(Exception):
    pass


class ContinueException(Exception):
    pass


class ReturnException(Exception):
    def __init__(self, val):
        self.val = val


class IndexOutOfBounds(Exception):
    def __init__(self, line, index, lower_bound, upper_bound):
        self.line = line
        self.index = index
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def __str__(self):
        return "{}Index {} out of bounds for range {}:{}".format(self.line, self.index, self.lower_bound, self.upper_bound)

