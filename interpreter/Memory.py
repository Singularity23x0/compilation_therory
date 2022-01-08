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
        self.data[name] = value
    # puts into memory current value of variable <name>


class MemoryStack:
    def __init__(self, memory=None):
        self.memory = []
        if memory is not None:
            self.memory.append(memory)

    # initialize memory stack with memory <memory>

    def get(self, name):
        for mem in reversed(self.memory):
            if mem.has_key(name):
                return mem.get(name)
        #  no error check already done is semanticChecker

    # gets from memory stack current value of variable <name>

    def has(self,name):
        for mem in reversed(self.memory):
            if mem.has_key(name):
                return True
        return False

    def insert(self, name, value):
        self.memory[-1].put(name, value)

    # inserts into memory stack variable <name> with value <value>

    def set(self, name, value):
        for mem in reversed(self.memory):
            if mem.has_key(name):
                return mem.put(name, value)
        #  no error check already done is semanticChecker

    # sets variable <name> to value <value>

    def push(self, memory):
        self.memory.append(memory)

    # pushes memory <memory> onto the stack

    def pop(self):
        self.memory.pop()
    # pops the top memory from the stack
