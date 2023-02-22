from variable import Variable
import sys
import errorCodes as err


class Frame:
    def __init__(self):
        self.__locals = dict()
        self._defined = False

    def AddVar(self, name):
        self.__locals[name] = Variable(name)

    def GetVar(self, name):
        try:
            return self.__locals[name]
        except:
            sys.exit(err.ERR_VARIABLE_NOT_FOUND)

    def GetVarValue(self, name):
        return self.__locals[name].value

    def GetVarType(self, name):
        return self.__locals[name].type

    @property
    def defined(self):
        return self._defined

    @defined.setter
    def defined(self, val):
        self._defined = val
