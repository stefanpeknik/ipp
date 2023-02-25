class Argument:
    def __init__(self, type: str, value):
        self._type = type
        self._value = value

    @property
    def type(self) -> str:
        return self._type

    @property
    def value(self):
        return self._value
