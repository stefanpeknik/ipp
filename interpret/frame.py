from interpret.variable import Variable


class Frame:
    def __init__(self):
        self.locals = dict()

    def AddVar(self, name):
        self.locals[name] = Variable(name)

    def GetVar(self, name):
        return self.locals[name]

    def IsVarDefined(self, name):
        return self.locals[name].IsDefined()
    
    def GetVarValue(self, name):
        return self.locals[name].value
    
    def GetVarType(self, name):
        return self.locals[name].type