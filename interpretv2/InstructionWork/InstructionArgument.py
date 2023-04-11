from InstructionWork.InstructionArgumentType import InstructionArgumentType
from Common.EscSeqTransformator import EscSeqTransformator
from Common.Mapper import Mapper
from InstructionWork.Exceptions import *
from Variable.DataType import DataType


class InstructionArgument:
    def __init__(self, argument_type: str, argument_value: str):
        if argument_type == "int":
            self.argument_type = InstructionArgumentType.INT
            self.argument_value = int(argument_value)
        elif argument_type == "bool":
            self.argument_type = InstructionArgumentType.BOOL
            self.argument_value = bool(argument_value)
        elif argument_type == "string":
            self.argument_type = InstructionArgumentType.STRING
            self.argument_value = EscSeqTransformator.transform(argument_value)
        elif argument_type == "nil":
            self.argument_type = InstructionArgumentType.NIL
            self.argument_value = None
        elif argument_type == "label":
            self.argument_type = InstructionArgumentType.LABEL
            self.argument_value = argument_value
        elif argument_type == "type":
            self.argument_type = InstructionArgumentType.TYPE
            self.argument_value = Mapper.map_string_to_dataType(argument_value)
        elif argument_type == "var":
            self.argument_type = InstructionArgumentType.VAR
            self.argument_value = argument_value
        else:
            raise InvalidXMLStructureException("Invalid argument type.")
