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
    def __init__(self, index, lower_bound, upper_bound):
        self.val = "Index {} out of bounds for range {}:{}".format(index, lower_bound, upper_bound)

