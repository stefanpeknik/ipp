from interpret.variable import Variable


class Frame:
    def __init__(self):
        self.__locals = dict()

    def AddVar(self, name):
        self.__locals[name] = Variable(name)

    def GetVar(self, name):
        return self.__locals[name]

    def GetVarValue(self, name):
        return self.__locals[name].value

    def GetVarType(self, name):
        return self.__locals[name].type
