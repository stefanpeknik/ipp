from interpret.errorCodes import ErrorCodes as err
from interpret.dataType import DataType


class Variable:

    def __init__(self, name):
        self._name = name
        self._inited = False

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value

    @property
    def type(self):
        return self._type

    @property
    def inited(self):
        return self._inited

    def set(self, type, val):
        self._type = type
        self._value = val
        self._inited = True

    # def __add__(self, other):
    #     if self.type == DataType.INT and other.type == DataType.INT:
    #         return self.value + other.value
    #     sys.exit(err.ERR_OPERAND_TYPE_ERROR)

    # def __sub__(self, other):
    #     if self.type == DataType.INT and other.type == DataType.INT:
    #         return self.value - other.value
    #     sys.exit(err.ERR_OPERAND_TYPE_ERROR)

    # def __mul__(self, other):
    #     if self.type == DataType.INT and other.type == DataType.INT:
    #         return self.value * other.value
    #     sys.exit(err.ERR_OPERAND_TYPE_ERROR)

    # def __truediv__(self, other):
    #     if self.type == DataType.INT and other.type == DataType.INT:
    #         if other.value == 0:
    #             sys.exit(err.ERR_INVALID_OPERAND_VALUE)
    #         return self.value / other.value
    #     sys.exit(err.ERR_OPERAND_TYPE_ERROR)

    # def __lt__(self, other):
    #     if self.type == DataType.INT and other.type == DataType.INT:
    #         return self.value < other.value
    #     if self.type == DataType.STRING and other.type == DataType.STRING:
    #         return self.value < other.value
    #     if self.type == DataType.BOOL and other.type == DataType.BOOL:
    #         if self.value == True and other.value == False:
    #             return False
    #         elif self.value == False and other.value == True:
    #             return True
    #         return False
    #     sys.exit(err.ERR_OPERAND_TYPE_ERROR)

    # def __gt__(self, other):
    #     if self.type == DataType.INT and other.type == DataType.INT:
    #         return self.value > other.value
    #     if self.type == DataType.STRING and other.type == DataType.STRING:
    #         return self.value > other.value
    #     if self.type == DataType.BOOL and other.type == DataType.BOOL:
    #         if self.value == True and other.value == False:
    #             return True
    #         elif self.value == False and other.value == True:
    #             return False
    #         return False
    #     sys.exit(err.ERR_OPERAND_TYPE_ERROR)

    # def __eq__(self, other):
    #     if self.type == DataType.INT and other.type == DataType.INT:
    #         return self.value == other.value
    #     if self.type == DataType.STRING and other.type == DataType.STRING:
    #         return self.value == other.value
    #     if self.type == DataType.BOOL and other.type == DataType.BOOL:
    #         return self.value == other.value
    #     return True

    # def And(self, other):
    #     if self.type == DataType.BOOL and other.type == DataType.BOOL:
    #         return self.value and other.value
    #     sys.exit(err.ERR_OPERAND_TYPE_ERROR)

    # def Or(self, other):
    #     if self.type == DataType.BOOL and other.type == DataType.BOOL:
    #         return self.value or other.value
    #     sys.exit(err.ERR_OPERAND_TYPE_ERROR)

    # def Not(self):
    #     if self.type == DataType.BOOL:
    #         return not self.value
    #     sys.exit(err.ERR_OPERAND_TYPE_ERROR)

    # def Int2Char(self):
    #     if self.type == DataType.INT:
    #         try:
    #             return chr(self.value)
    #         except ValueError:
    #             sys.exit(err.ERR_STRING_ERROR)
    #     sys.exit(err.ERR_OPERAND_TYPE_ERROR)

    # def Str2Int(self):
    #     if self.type == DataType.STRING:
    #         try:
    #             return ord(self.value)
    #         except ValueError:
    #             sys.exit(err.ERR_STRING_ERROR)
    #     sys.exit(err.ERR_OPERAND_TYPE_ERROR)
