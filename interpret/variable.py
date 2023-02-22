class Variable:

    def __init__(self, name):
        self._name = name
        self._inited = False

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value

    @property
    def type(self):
        return self._type

    @property
    def inited(self):
        return self._inited

    def set(self, type, val):
        self._type = type
        self._value = val
        self._inited = True
