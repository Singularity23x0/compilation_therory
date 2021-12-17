class Memory:
    def __init__(self, name):
        self.name = name
        self.data = dict()

    # memory name

    def has_key(self, name):
        return name in self.data

    # variable name

    def get(self, name):
        return self.data.get(name)

    # gets from memory current value of variable <name>

    def put(self, name, value):
        return self.data.put(name, value)
    # puts into memory current value of variable <name>


class MemoryStack:
    def __init__(self, memory=None):
        self.memory = Memory("variables") if memory is None else memory

    # initialize memory stack with memory <memory>

    def get(self, name):
        return self.memory.get(name)

    # gets from memory stack current value of variable <name>

    def insert(self, name, value):
        pass

    # inserts into memory stack variable <name> with value <value>

    def set(self, name, value):
        pass

    # sets variable <name> to value <value>

    def push(self, memory):
        pass

    # pushes memory <memory> onto the stack

    def pop(self):
        pass
    # pops the top memory from the stack
