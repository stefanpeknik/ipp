from Value import Value
from VariableNotInitedException import VariableNotInitedException


class Variable:
    def __init__(self, name: str):
        self._name = name
        self._inited = False

    @property
    def name(self) -> str:
        return self._name

    @property
    def value(self) -> Value:
        if not self._inited:
            raise VariableNotInitedException(
                "Variable {} not inited.".format(self._name))
        return self._value

    @value.setter
    def value(self, value: Value) -> None:
        self._value = value
        self._inited = True

    @property
    def inited(self) -> bool:
        return self._inited
