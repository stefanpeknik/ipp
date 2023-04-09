from Variable.Variable import Variable
from VariableNotInFrameException import VariableNotInFrameException


class Frame:
    def __init__(self):
        self.__locals = dict()
        self._defined = False

    def AddVar(self, var: Variable):
        self.__locals[var.name] = var

    def GetVarByName(self, name: str):
        try:
            return self.__locals[name]
        except:
            raise VariableNotInFrameException(
                "Variable {} not found in frame.".format(name))

    @property
    def defined(self):
        return self._defined

    @defined.setter
    def defined(self, defined: bool):
        self._defined = defined
