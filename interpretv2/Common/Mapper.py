from InstructionWork.InstructionArgumentType import InstructionArgumentType
from Variable.DataType import DataType


class Mapper:
    @staticmethod
    def map_instrucArgType_to_dataType(instrucArgType: InstructionArgumentType):
        if instrucArgType == InstructionArgumentType.INT:
            return DataType.int
        elif instrucArgType == InstructionArgumentType.BOOL:
            return DataType.bool
        elif instrucArgType == InstructionArgumentType.STRING:
            return DataType.string
        elif instrucArgType == InstructionArgumentType.NIL:
            return DataType.nil

    @staticmethod
    def map_dataType_to_string(dataType: DataType):
        if dataType == DataType.int:
            return "int"
        elif dataType == DataType.bool:
            return "bool"
        elif dataType == DataType.string:
            return "string"
        elif dataType == DataType.nil:
            return "nil"

    @staticmethod
    def map_string_to_dataType(string: str):
        if string == "int":
            return DataType.int
        elif string == "bool":
            return DataType.bool
        elif string == "string":
            return DataType.string
        elif string == "nil":
            return DataType.nil

