from interpret.variable import Variable


class Frame:
    def __init__(self):
        self.locals = dict()

    def AddVar(self, name, value, type):
        self.locals[name] = Variable(name, value, type)

    def GetVar(self, name):
        return self.locals[name]
