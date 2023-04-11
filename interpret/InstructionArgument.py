from InstructionArgumentType import InstructionArgumentType
from ValueParser import ValueParser

from Exceptions import InvalidXMLStructureException


class InstructionArgument:
    def __init__(self, argument_type: str, argument_value: str | None):
        if argument_value is None:  # if argument is empty
            argument_value = ""

        if argument_type == "int":
            self.argument_type = InstructionArgumentType.INT
            self.argument_value = ValueParser.parse_int(argument_value)
        elif argument_type == "bool":
            self.argument_type = InstructionArgumentType.BOOL
            self.argument_value = ValueParser.parse_bool(argument_value)
        elif argument_type == "string":
            self.argument_type = InstructionArgumentType.STRING
            self.argument_value = ValueParser.parse_string(argument_value)
        elif argument_type == "nil":
            self.argument_type = InstructionArgumentType.NIL
            self.argument_value = ValueParser.parse_nil(argument_value)
        elif argument_type == "label":
            self.argument_type = InstructionArgumentType.LABEL
            self.argument_value = ValueParser.parse_label(argument_value)
        elif argument_type == "type":
            self.argument_type = InstructionArgumentType.TYPE
            self.argument_value = ValueParser.parse_type(argument_value)
        elif argument_type == "var":
            self.argument_type = InstructionArgumentType.VAR
            self.argument_value = ValueParser.parse_var(argument_value)
        else:
            raise InvalidXMLStructureException("Invalid argument type.")
