from Variable.DataType import DataType


class Value:
    def __init__(self, type: DataType, value):
        self._type = type
        self._value = value

    @property
    def type(self) -> DataType:
        return self._type

    @property
    def value(self):
        return self._value
