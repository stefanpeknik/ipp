from Variable.DataType import DataType

from InstructionWork.Exceptions import MissingValueException


class Variable:
    def __init__(self, name: str):
        self._name = name
        self._type = DataType.int  # dummy value
        self._inited = False

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> DataType:
        if not self._inited:
            raise MissingValueException(
                "Variable {} not inited.".format(self._name))
        return self._type

    @type.setter
    def type(self, type: DataType) -> None:
        self._type = type

    @property
    def value(self):
        if not self._inited:
            raise MissingValueException(
                "Variable {} not inited.".format(self._name))
        return self._value

    @value.setter
    def value(self, value) -> None:
        self._value = value
        self._inited = True

    @property
    def inited(self) -> bool:
        return self._inited

    @inited.setter
    def inited(self, inited: bool) -> None:
        self._inited = inited
