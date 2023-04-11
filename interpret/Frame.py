from Variable import Variable

from Exceptions import SemanticException, UndefinedVariableException


class Frame:
    def __init__(self):
        self.__locals = dict()

    def AddVar(self, var: Variable):
        if self.IsVarInFrame(var.name):
            raise SemanticException(
                "Variable {} already defined in frame.".format(var.name))
        self.__locals[var.name] = var

    def GetVarByName(self, name: str) -> Variable:
        var = self.__locals.get(name)
        if var is None:
            raise UndefinedVariableException(
                "Variable {} not found in frame.".format(name))
        return var

    def IsVarInFrame(self, name: str):
        return name in self.__locals

    def GetLocals(self):
        return self.__locals
