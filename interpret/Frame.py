from Variable import Variable

from Exceptions import SemanticException, UndefinedVariableException


class Frame:
    def __init__(self):
        self.__locals = dict()

    def add_var(self, var: Variable):
        if self.is_var_in_frame(var.name):
            raise SemanticException(
                "Variable {} already defined in frame.".format(var.name))
        self.__locals[var.name] = var

    def get_var_by_name(self, name: str) -> Variable:
        var = self.__locals.get(name)
        if var is None:
            raise UndefinedVariableException(
                "Variable {} not found in frame.".format(name))
        return var

    def is_var_in_frame(self, name: str):
        return name in self.__locals

    def get_locals(self):
        return self.__locals
